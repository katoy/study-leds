import math

class Point3D:
    DEG_TO_RAD = math.pi / 180  # キャッシュして再利用

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x, self.y, self.z = x, y, z

    def _rotate(self, angle: float, axis: str) -> 'Point3D':
        """ 共通の回転ロジック。軸 (X, Y, Z) に応じて回転を適用 """
        rad = angle * self.DEG_TO_RAD
        cosa = math.cos(rad)
        sina = math.sin(rad)

        if axis == 'x':
            y = self.y * cosa - self.z * sina
            z = self.y * sina + self.z * cosa
            return Point3D(self.x, y, z)
        elif axis == 'y':
            z = self.z * cosa - self.x * sina
            x = self.z * sina + self.x * cosa
            return Point3D(x, self.y, z)
        elif axis == 'z':
            x = self.x * cosa - self.y * sina
            y = self.x * sina + self.y * cosa
            return Point3D(x, y, self.z)
        else:
            raise ValueError("Invalid axis. Choose 'x', 'y', or 'z'.")

    def rotate_x(self, angle: float) -> 'Point3D':
        """ X 軸周りに指定された角度で回転 """
        return self._rotate(angle, 'x')

    def rotate_y(self, angle: float) -> 'Point3D':
        """ Y 軸周りに指定された角度で回転 """
        return self._rotate(angle, 'y')

    def rotate_z(self, angle: float) -> 'Point3D':
        """ Z 軸周りに指定された角度で回転 """
        return self._rotate(angle, 'z')

    def project(self, win_width: float, win_height: float, fov: float, viewer_distance: float) -> 'Point3D':
        """ この 3D ポイントを透視投影して2Dに変換する """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)


if __name__ == "__main__":
    def main():
        # 初期座標の設定
        point = Point3D(1, 2, 3)
        print(f"Original Point: {point.x}, {point.y}, {point.z}")

        # X軸周りに回転
        rotated_x = point.rotate_x(90)
        print(f"After X Rotation: {rotated_x.x}, {rotated_x.y}, {rotated_x.z}")

        # Y軸周りに回転
        rotated_y = point.rotate_y(90)
        print(f"After Y Rotation: {rotated_y.x}, {rotated_y.y}, {rotated_y.z}")

        # Z軸周りに回転
        rotated_z = point.rotate_z(90)
        print(f"After Z Rotation: {rotated_z.x}, {rotated_z.y}, {rotated_z.z}")

        # 透視投影
        win_width, win_height = 800, 600
        fov, viewer_distance = 256, 5
        projected = point.project(win_width, win_height, fov, viewer_distance)
        print(f"Projected Point: {projected.x}, {projected.y}, {projected.z}")

    main()

