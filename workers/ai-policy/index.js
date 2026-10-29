export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    try {
      const data = await request.json();
      
      const ilbLine = data.ilb 
        ? `- Inflation-linked bond (reference): cost ${data.ilb.cost.toFixed(3)}, distress ${(data.ilb.distress * 100).toFixed(1)}%`
        : `- Inflation-linked bond: not computed`;

      const prompt = `You are a sovereign debt advisor. Analyze this Policy Lab scenario:

SOVEREIGN PROFILE:
- Debt/GDP: ${data.scenario.debtGDP}%
- Nominal growth: ${(data.scenario.muY * 100).toFixed(1)}%
- Inflation: ${(data.scenario.muPi * 100).toFixed(1)}%
- NPI growth: ${(data.scenario.muN * 100).toFixed(1)}%

BOND COMPARISON (endogenous debt model, 10-year horizon):
- Conventional bond: cost ${data.conventional.cost.toFixed(3)}, distress ${(data.conventional.distress * 100).toFixed(1)}%
- Productivity bond: cost ${data.productivity.cost.toFixed(3)}, distress ${(data.productivity.distress * 100).toFixed(1)}%
${ilbLine}

POLICY LEVERS:
- Principal-Adjustment Mechanism (PAM): ${data.scenario.pam ? "enabled" : "disabled"}
- Government capture of AI gains (theta_AI): ${data.scenario.thetaAI}
- Recommended portfolio share: ${(data.optimalShare * 100).toFixed(0)}%

DETERMINISTIC VERDICT (from rule engine): ${data.verdict}

Write a 2-sentence summary of the key trade-off, then 1 sentence of concrete policy recommendation. Be direct and professional. Do not invent numbers not provided.`;

      const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.GROQ_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "llama3-8b-8192",
          messages: [{ role: "user", content: prompt }],
          temperature: 0.6,
          max_tokens: 250
        })
      });

      if (!response.ok) {
        const errText = await response.text();
        return new Response(JSON.stringify({ error: 'Groq API error: ' + errText }), { 
          status: 500, 
          headers: { "Content-Type": "application/json" } 
        });
      }

      const result = await response.json();
      const aiText = result.choices[0].message.content.trim();

      // Split into summary (first 2 sentences) and advice (rest)
      const sentences = aiText.match(/[^.!?]+[.!?]+/g) || [aiText];
      const summary = sentences.slice(0, 2).join(' ').trim();
      const advice = sentences.slice(2).join(' ').trim() || "Review the recommended portfolio share before issuance.";

      return new Response(JSON.stringify({ summary, advice }), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });

    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), { 
        status: 500, 
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } 
      });
    }
  }
};
