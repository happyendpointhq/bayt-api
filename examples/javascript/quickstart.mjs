// Bayt.com Jobs API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs ae dubai

const HOST = 'bayt-com.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Bayt API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const [country = 'ae', citySlug = 'dubai'] = process.argv.slice(2);
const { cities } = await get('/cities', { country });
const city = cities.find((c) => c.slug === citySlug);
if (!city) throw new Error(`No city ${citySlug} in ${country}`);
console.log(`${city.name} (id ${city.id}): ${city.jobsCount} jobs`);

const results = await get('/job-search', { city: city.id, date_posted: '2' });
console.log(`${results.count} jobs posted in the past 7 days`);
for (const job of results.jobs.slice(0, 10)) {
  const employer = job.company?.isConfidential ? 'Confidential' : job.company?.name;
  console.log(`${job.postedAt.slice(0, 10)}  ${job.title}  (${employer})  ${job.salary?.formatted ?? ''}`);
}
