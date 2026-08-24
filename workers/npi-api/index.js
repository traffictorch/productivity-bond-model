cat > index.js << 'EOF'
// workers/npi-api/index.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    const corsHeaders = {
      "Access-Control-Allow-Origin": "https://traffictorch.github.io",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (path === "/api/countries") {
      const stmt = env.NPI_DB.prepare("SELECT DISTINCT country_code FROM 
npi_series ORDER BY country_code");
      const { results } = await stmt.all();
      return Response.json(results.map(r => r.country_code), { headers: 
corsHeaders });
    }

    if (path === "/api/npi") {
      const country = url.searchParams.get("country");
      const start = parseInt(url.searchParams.get("start")) || 1990;
      const end = parseInt(url.searchParams.get("end")) || 2023;
      if (!country) {
        return new Response("Missing country", { status: 400, headers: 
corsHeaders });
      }
      const stmt = env.NPI_DB.prepare("SELECT year, gdp, hours, energy, 
materials, capital FROM npi_series WHERE country_code = ? AND year BETWEEN ? 
AND ? ORDER BY year");
      const { results } = await stmt.bind(country, start, end).all();
      return Response.json(results, { headers: corsHeaders });
    }

    return new Response("Not Found", { status: 404, headers: corsHeaders });
  }
};
EOF
