# SmartHR IME Dictionary

Create an IME dictionary using the [SmartHR API](https://developer.smarthr.jp).

# Requirements

- Python (3.6 or higher)
- [Dependencies](./requirements.txt)

# Usage

Set the following environment variables:

- `SMARTHR_TENANT`
- `SMARTHR_TOKEN`

Refer to `python create_dict.py --help` for more information.

Check the links below for instructions on setting up the IME for your specific operating system:

- [macOS](https://support.apple.com/ja-jp/guide/japanese-input-method/jpim10226/mac) (Use CSV or plist format)
- [Google Japanese IME](https://support.google.com/ime/japanese/answer/166765?hl=ja) (Use TSV format)
- [Mozc](https://wiki.archlinux.jp/index.php/Mozc) (Use TSV format)
- [MS IME](https://support.microsoft.com/ja-jp/windows/microsoft-%E6%97%A5%E6%9C%AC%E8%AA%9E-ime-da40471d-6b91-4042-ae8b-713a96476916)

## Using Docker

```console
docker run --rm -e SMARTHR_TENANT=$SMARTHR_TENANT -e SMARTHR_TOKEN=$SMARTHR_TOKEN ghcr.io/yasuyuky/smarthr-imedic csv > ime.csv
```
