import httpx
from pathlib import Path

data_url = "https://mrv.emsa.europa.eu/api/public-emission-report/reporting-period-document/binary/"
data_dir = Path("/data/raw").absolute()
if not data_dir.exists():
    data_dir.mkdir(parents=True, exist_ok=True)

year = 2018
while True:
    file_path = data_dir / f"{year}.xlsx"
    if file_path.exists():
        print(f"{year} already exists.")
    else:
        response = httpx.get(data_url + str(year))
        if response.status_code == 200:
            print(f"Downloading data for {year}...")
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            break
    year += 1
