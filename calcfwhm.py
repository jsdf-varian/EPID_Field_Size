import numpy as np


def calculate_fwhm(line_profile, pixel_spacing):
    # 中心の最大値の半分（FWHM）を設定
    half_max = np.max(line_profile) / 2

    # 配列のインデックスを取得
    indices = np.arange(len(line_profile))

    # Half Maximumを超える点を見つける
    above_half = line_profile >= half_max

    # 左側のFWHM位置を見つける
    left_idx = indices[above_half][0]
    if left_idx > 0:  # 補間のため1つ前の点も使用
        left_prev = left_idx - 1
        # 線形補間
        left_pos = left_prev + (half_max - line_profile[left_prev]) / (
            line_profile[left_idx] - line_profile[left_prev]
        )
    else:
        left_pos = left_idx

    # 右側のFWHM位置を見つける
    right_idx = indices[above_half][-1]
    if right_idx < len(line_profile) - 1:  # 補間のため1つ後の点も使用
        right_next = right_idx + 1
        # 線形補間
        right_pos = right_idx + (half_max - line_profile[right_idx]) / (
            line_profile[right_next] - line_profile[right_idx]
        )
    else:
        right_pos = right_idx

    # FWHMを計算（ピクセル間隔を考慮）
    fwhm = (right_pos - left_pos) * pixel_spacing

    return fwhm, left_pos, right_pos
