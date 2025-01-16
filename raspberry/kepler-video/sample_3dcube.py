from machine import I2C, Pin
import ssd1306
from point3d import Point3D

class Simulation:
    def __init__(self, width=128, height=64, fov=64, distance=4, rotate_x=5, rotate_y=5, rotate_z=5):
        # 頂点リストを定義
        self.vertices = [
            Point3D(-1, 1, -1),
            Point3D( 1, 1, -1),
            Point3D( 1, -1, -1),
            Point3D(-1, -1, -1),
            Point3D(-1, 1, 1),
            Point3D( 1, 1, 1),
            Point3D( 1, -1, 1),
            Point3D(-1, -1, 1)
        ]

        # 辺を定義（各ペアは `vertices` のインデックス）
        self.edges = [
            # 背面
            (0, 1), (1, 2), (2, 3), (3, 0),
            # 前面
            (5, 4), (4, 7), (7, 6), (6, 5),
            # 前面と背面をつなぐ線
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]

        # プロジェクションのパラメータ（画面幅、高さ、視野角、視点距離）
        self.projection = [width, height, fov, distance]

        # 各軸の回転速度
        self.rotate_x = rotate_x
        self.rotate_y = rotate_y
        self.rotate_z = rotate_z

    @staticmethod
    def to_int(*args):
        """引数を整数に変換するユーティリティ関数"""
        return [int(v) for v in args]

    def run(self):
        # 初期角度（X軸、Y軸、Z軸の回転）
        angle_x, angle_y, angle_z = 0, 0, 0

        while True:
            transformed_vertices = []
            for vertex in self.vertices:
                # 頂点をX軸、Y軸、Z軸で順に回転
                rotated_vertex = (
                    vertex.rotate_x(angle_x)
                          .rotate_y(angle_y)
                          .rotate_z(angle_z)
                )

                # 3D座標を2D座標に変換（透視投影）
                projected_vertex = rotated_vertex.project(*self.projection)

                # 変換した頂点をリストに追加
                transformed_vertices.append(projected_vertex)

            display.fill(0)  # 画面をクリア

            for edge in self.edges:
                # 頂点間をつなぐ線を描画
                start = transformed_vertices[edge[0]]
                end = transformed_vertices[edge[1]]
                display.line(*self.to_int(start.x, start.y, end.x, end.y, 1))

            display.show()  # 描画を反映

            # 回転角度を更新
            angle_x += self.rotate_x
            angle_y += self.rotate_y
            angle_z += self.rotate_z


# ディスプレイの初期化
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=200000)  # SDA: GPIO2, SCL: GPIO3
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# シミュレーションの実行
simulation = Simulation(fov=400, distance=25)  # 視野角と距離を設定
simulation.run()
