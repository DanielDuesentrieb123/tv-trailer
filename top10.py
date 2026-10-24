"""Netflix's official weekly Top 10 for one country, as a small JSON file for Free My TV.

Netflix publishes the Top 10 of every country in one file of about 30 MB (all weeks, all countries); a TV shouldn't
load that. This keeps the latest week of one country:
    python3 top10.py out.json [DE]
→ {"country": "DE", "week": "2026-10-18", "films": [{"rank": 1, "title": "..."}], "tv": [{"rank": 1, "title": "...",
   "season": "..."}]}
If Netflix can't be reached, the file already published is kept, so the site still deploys.
"""
import csv, io, json, sys, urllib.request

SOURCE = 'https://www.netflix.com/tudum/top10/data/all-weeks-countries.tsv'
PUBLISHED = 'https://danielduesentrieb123.github.io/tv-trailer/top10.json'


def latest(country):
    rows, week = [], ''
    with urllib.request.urlopen(SOURCE, timeout=120) as response:
        lines = io.TextIOWrapper(response, encoding='utf-8')
        for row in csv.DictReader(lines, delimiter='\t'):
            if row['country_iso2'] != country:
                continue
            if row['week'] > week:
                week, rows = row['week'], []
            if row['week'] == week:
                rows.append(row)
    if not rows:
        raise RuntimeError('no Top 10 for ' + country)

    def entries(category):
        out = []
        for r in sorted((r for r in rows if r['category'] == category), key=lambda r: int(r['weekly_rank'])):
            e = {'rank': int(r['weekly_rank']), 'title': r['show_title']}
            if r.get('season_title') and r['season_title'] != 'N/A':
                e['season'] = r['season_title']
            out.append(e)
        return out

    return {'country': country, 'week': week, 'films': entries('Films'), 'tv': entries('TV')}


def main():
    out = sys.argv[1]
    country = sys.argv[2] if len(sys.argv) > 2 else 'DE'
    try:
        data = latest(country)
    except Exception as e:
        print('Netflix not reachable (%s): keeping the published file' % e)
        with urllib.request.urlopen(PUBLISHED, timeout=30) as response:
            data = json.load(response)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print('Top 10 %s, week of %s: %d films, %d shows' % (data['country'], data['week'], len(data['films']), len(data['tv'])))


if __name__ == '__main__':
    main()
