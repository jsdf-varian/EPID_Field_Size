import numpy as np
import matplotlib.pyplot as plt
import pydicom

from calcfwhm import calculate_fwhm


def main(file_name, figure=False):
    data = pydicom.dcmread(file_name, force=True)
    pixel_spacing = float(data[0x30020011].value[0])
    rows = int(data[0x00280010].value)
    cols = int(data[0x00280011].value)
    row_center = rows // 2
    col_center = cols // 2

    # 画像の読み込み
    array = data.pixel_array

    # 中心座標で正規化
    center_value = array[row_center, col_center]
    normalize_array = array / center_value

    center_value = normalize_array[row_center, col_center]
    col_line = normalize_array[:, col_center]
    row_line = normalize_array[row_center, :]

    # 行方向と列方向のFWHMを計算
    col_fwhm, col_left, col_right = calculate_fwhm(col_line, pixel_spacing)
    row_fwhm, row_left, row_right = calculate_fwhm(row_line, pixel_spacing)

    print(f"In-line FWHM: {col_fwhm:.2f} mm")
    print(f"Cross-line FWHM: {row_fwhm:.2f} mm")

    if figure:
        # プロットして確認
        # 列方向のプロット
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(col_line)
        plt.axhline(
            y=np.max(col_line) / 2, color="r", linestyle="--", label="Half Maximum"
        )
        plt.axvline(x=col_left, color="g", linestyle="--", label="Left FWHM")
        plt.axvline(x=col_right, color="g", linestyle="--", label="Right FWHM")
        plt.title("Inline Profile")
        plt.legend()

        # 行方向のプロット
        plt.subplot(1, 2, 2)
        plt.plot(row_line)
        plt.axhline(
            y=np.max(row_line) / 2, color="r", linestyle="--", label="Half Maximum"
        )
        plt.axvline(x=row_left, color="g", linestyle="--", label="Left FWHM")
        plt.axvline(x=row_right, color="g", linestyle="--", label="Right FWHM")
        plt.title("Cross Profile")
        plt.legend()

        plt.tight_layout()
        plt.show()
        
    return col_fwhm, row_fwhm
