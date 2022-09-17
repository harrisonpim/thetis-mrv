import httpx
from pathlib import Path

data_url = "https://mrv.emsa.europa.eu/api/public-emission-report/reporting-period-document/binary/"


data_dir = Path("/data/").absolute()
if not data_dir.exists():
    data_dir.mkdir(parents=True)


for year in range(2018, 2022):
    file_path = data_dir / "raw" / f"{year}.xlsx"
    if not file_path.exists():
        print(f"Downloading {year}...")
        Path(file_path).parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, "wb") as f:
            url = data_url + str(year)
            file_data = httpx.get(url).content
            f.write(file_data)
    else:
        print(f"{year} already exists.")
