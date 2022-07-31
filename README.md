# SmartHR IME dict

Create IME dictionary from [API of SmartHR](https://developer.smarthr.jp)

# Requirements

- Python (3.6 or above)
- [deps](./requirements.txt)

# Usage

Set the following environment variables

- `SMARTHR_TENANT`
- `SMARTHR_TOKEN`

See `python create_dict.py --help`

Please check the following link for instructions on how to set up the IME you are using.

- [macOS](https://support.apple.com/ja-jp/guide/japanese-input-method/jpim10226/mac) (Use csv (or plist))
- [Google Japanese IME](https://support.google.com/ime/japanese/answer/166765?hl=ja) (Use tsv)
- [Mozc](https://wiki.archlinux.jp/index.php/Mozc) (Use tsv)
- [MS IME](https://support.microsoft.com/ja-jp/windows/microsoft-%E6%97%A5%E6%9C%AC%E8%AA%9E-ime-da40471d-6b91-4042-ae8b-713a96476916)

## With Docker

```console
docker run --rm -e SMARTHR_TENANT=$SMARTHR_TENANT -e SMARTHR_TOKEN=$SMARTHR_TOKEN ghcr.io/yasuyuky/smarthr-imedic csv > ime.csv
```
