const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400"
};

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...CORS }
  });

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS });
    }
    if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);

    try {
      const data = await request.json();
      const scenario = data.scenario || {};
      const conventional = data.conventional || {};
      const productivity = data.productivity || {};
      const ilb = data.ilb || null;

      // Build bond list
      const bonds = [
        { name: "Conventional", cost: conventional.cost, distress: conventional.distress },
        { name: "Productivity", cost: productivity.cost, distress: productivity.distress }
      ];
      if (ilb) bonds.push({ name: "Inflation-linked", cost: ilb.cost, distress: ilb.distress });

      // Pre-computed rankings — LLM cannot mis-order these
      const costRank = [...bonds].sort((a, b) => a.cost - b.cost)
        .map(b => `  • ${b.name}: cost ${b.cost.toFixed(3)}`).join('\n');
      const distressRank = [...bonds].sort((a, b) => a.distress - b.distress)
        .map(b => `  • ${b.name}: distress ${(b.distress * 100).toFixed(1)}%`).join('\n');

      // Dominance classification
      let dominanceLine = "";
      if (ilb) {
        const ilbCheaper = ilb.cost < conventional.cost && ilb.cost < productivity.cost;
        const ilbSafer = ilb.distress < conventional.distress && ilb.distress < productivity.distress;
        if (ilbCheaper && ilbSafer) {
          dominanceLine = "ILB DOMINANCE: FULL — ILB is BOTH cheapest and safest.";
        } else if (ilbCheaper) {
          dominanceLine = "ILB DOMINANCE: COST — ILB is cheapest but not safest.";
        } else if (ilbSafer) {
          dominanceLine = "ILB DOMINANCE: SAFETY — ILB is safest but not cheapest.";
        } else {
          dominanceLine = "ILB DOMINANCE: NONE.";
        }
      }

      const optimalPct = (data.optimalShare * 100).toFixed(0);

      const prompt = `You are a sovereign debt advisor. Analyze this Policy Lab scenario.

SOVEREIGN PROFILE:
- Debt/GDP: ${scenario.debtGDP}%
- Nominal growth: ${(scenario.muY * 100).toFixed(1)}%
- Inflation: ${(scenario.muPi * 100).toFixed(1)}%
- NPI growth: ${(scenario.muN * 100).toFixed(1)}%

BOND DATA (10-year endogenous debt model):
${bonds.map(b => `- ${b.name}: cost ${b.cost.toFixed(3)}, distress ${(b.distress * 100).toFixed(1)}%`).join('\n')}

EXPLICIT RANKINGS — USE THESE VERBATIM, DO NOT RE-DERIVE:
Cost ranking (cheapest first):
${costRank}

Distress ranking (safest first):
${distressRank}

POLICY LEVERS:
- PAM: ${scenario.pam ? "enabled" : "disabled"}
- theta_AI (AI gain capture): ${scenario.thetaAI}
- Portfolio optimizer recommends ${optimalPct}% of NEW issuance in PRODUCTIVITY bonds. This is NOT an ILB allocation.

RULE-ENGINE VERDICT: ${data.verdict}
${dominanceLine}

Respond in EXACTLY this format, nothing before or after:
SUMMARY: <two sentences in prose form. Do not include bullet characters, rank numbers, or list formatting. When naming which bond is cheapest, use the cost ranking verbatim. When naming which is safest, use the distress ranking verbatim.>
RECOMMENDATION: <one sentence of concrete policy advice. Rules: (a) If conventional distress > 50%, say the optimizer is unreliable in this regime and advise fixing the primary balance. (b) If a bond is both cheapest AND safest, recommend that bond — ignore the ${optimalPct}% optimizer share as it conflicts with the ranking. (c) If ILB dominance is FULL, recommend the ILB.>`;

      const response = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
        messages: [{ role: "user", content: prompt }],
        temperature: 0.3,
        max_tokens: 300
      });

      const aiText = (response.response || "").trim();
      if (!aiText) throw new Error("Empty response from Workers AI");

      let summary = "", advice = "";
      const sumMatch = aiText.match(/SUMMARY:\s*([\s\S]+?)(?=\n?RECOMMENDATION:|$)/i);
      const recMatch = aiText.match(/RECOMMENDATION:\s*([\s\S]+?)$/i);

      if (sumMatch && recMatch) {
        summary = sumMatch[1].trim();
        advice  = recMatch[1].trim();
      } else {
        const sentences = aiText.match(/[^.!?]+[.!?]+(?=\s+[A-Z]|\s*$)/g) || [aiText];
        summary = sentences.slice(0, 2).join(" ").trim();
        advice  = sentences.slice(2).join(" ").trim()
               || "Review the recommended portfolio share before issuance.";
      }

      return json({ summary, advice });

    } catch (error) {
      return json({ error: error.message }, 500);
    }
  }
};
