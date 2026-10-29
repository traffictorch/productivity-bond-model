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

      const ilbLine = ilb
        ? `- Inflation-linked bond: cost ${ilb.cost.toFixed(3)}, distress ${(ilb.distress * 100).toFixed(1)}%`
        : `- Inflation-linked bond: not computed`;

      // Compute dominance explicitly so the LLM cannot miss it
      let dominanceLine = "";
      if (ilb) {
        const ilbCheaper = ilb.cost < conventional.cost && ilb.cost < productivity.cost;
        const ilbSafer = ilb.distress < conventional.distress && ilb.distress < productivity.distress;
        if (ilbCheaper && ilbSafer) {
          dominanceLine = "\nILB DOMINANCE: YES. The inflation-linked bond is BOTH cheaper and less distress-prone than every other option. Your recommendation MUST state this and recommend the ILB.";
        } else if (ilbCheaper || ilbSafer) {
          dominanceLine = "\nILB DOMINANCE: PARTIAL. The ILB wins on one dimension but not both. Mention the specific trade-off.";
        } else {
          dominanceLine = "\nILB DOMINANCE: NO. The ILB does not beat the alternatives on both dimensions.";
        }
      }

      const prompt = `You are a sovereign debt advisor. Analyze this Policy Lab scenario.

SOVEREIGN PROFILE:
- Debt/GDP: ${scenario.debtGDP}%
- Nominal growth: ${(scenario.muY * 100).toFixed(1)}%
- Inflation: ${(scenario.muPi * 100).toFixed(1)}%
- NPI growth: ${(scenario.muN * 100).toFixed(1)}%

BOND COMPARISON (endogenous debt model, 10-year horizon):
- Conventional bond: cost ${conventional.cost.toFixed(3)}, distress ${(conventional.distress * 100).toFixed(1)}%
- Productivity bond: cost ${productivity.cost.toFixed(3)}, distress ${(productivity.distress * 100).toFixed(1)}%
${ilbLine}

POLICY LEVERS:
- Principal-Adjustment Mechanism (PAM): ${scenario.pam ? "enabled" : "disabled"}
- Government capture of AI gains (theta_AI): ${scenario.thetaAI}
- Recommended portfolio share: ${(data.optimalShare * 100).toFixed(0)}%

RULE-ENGINE VERDICT: ${data.verdict}
${dominanceLine}

Respond in EXACTLY this format, nothing before or after:
SUMMARY: <two sentences describing the key trade-off, using only the numbers above>
RECOMMENDATION: <one sentence of concrete policy advice. If ILB dominance is YES, recommend the ILB.>`;

      const response = await env.AI.run("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
        messages: [{ role: "user", content: prompt }],
        temperature: 0.4,
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
