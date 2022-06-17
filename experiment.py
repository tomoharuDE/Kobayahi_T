import tkinter as tk
import PIL.Image, PIL.ImageTk
import tobii_research as tr
import time
import pandas as pd
import pyautogui
from datetime import datetime
from pynput import mouse, keyboard
import threading


# import os


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # ウィンドウタイトルを決定
        self.title("図形描画課題プログラミング")

        # ウィンドウの大きさを決定
        self.geometry("1265x1300+0+0")

        # ウィンドウのグリッドを 1x1 にする
        # この処理をコメントアウトすると配置がズレる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # -----------------------------------frame1-----------------------------
        # メインページフレーム作成
        self.frame1 = tk.Frame()
        self.frame1.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.frame1, text="Hello, world.", font=('Helvetica', '35'))
        self.titleLabel.pack(anchor='n')

        self.thankLabel = tk.Label(self.frame1, text="研究にご協力ありがとうございます。\n", justify='left', font=('Helvetica', '12'))
        self.thankLabel.pack(anchor='n', expand=True)

        self.introLabel = tk.Label(self.frame1,
                                   text="このページは課題表示用のページです。\n画面内に表示されるボタンでのみ操作可能です。\nウインドウサイズはそのままにしてください。\n（消去しないよう注意）",
                                   justify='left', font=('Helvetica', '12'))
        self.introLabel.pack(anchor='n', expand=True)

        self.dataLabel = tk.Label(self.frame1,
                                  text="研究データの取り扱い\nプログラミング時のPC操作に関するデータを収集します。\nデータを研究以外で用いることはしませんが、\nその一部または評価結果は公表する場合があります。",
                                  justify='left', font=('Helvetica', '12'))
        self.dataLabel.pack(anchor='n', expand=True)
        # フレーム1に移動するボタン
        self.changePageButton = tk.Button(self.frame1, text="START", command=lambda: self.changePage(self.frame2))
        self.changePageButton.pack()
        # --------------------------------------------------------------------------
        # -----------------------------------frame2---------------------------------
        # 移動先フレーム作成
        self.frame2 = tk.Frame()
        self.frame2.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.frame2, text="Q1:繰り返し\n正三角形", font=('Helvetica', '24'))
        self.titleLabel.pack(anchor='n', expand=True)

        self.textLabel = tk.Label(self.frame2, text="図のような形状を正三角形の繰り返しで表現する。\n"
                                                    "使用する描画関数はforward()とleft()である\n"
                                                    "なお、カメの初期位置は中心であり、3時方向を向いている。\n\n"
                                                    "まず、基準となる正三角形は一辺の長さが60であり、\n"
                                                    "描画枠の中心が上側頂点であり、そこを始点として\n"
                                                    "時計回り方向に3回辺を書くことを繰り返して描画される。\n\n"
                                                    "次に描画する正三角形は前のものより長さを10増やす。\n"
                                                    "さらに、前の三角形より1回多く同じ方向に辺をなぞる。\n"
                                                    "これにより次の始点がずれつつ、段差のような形状が生まれる。\n\n"
                                                    "今回はこれらの正三角形を9回描画するが、3,6,9...のように\n"
                                                    "なぞる回数が3で割り切れる数のときは、次の始点がずれない。\n"
                                                    "この場合は長さを増やさずに前と同じ三角形をなぞることとする。\n", justify='left',
                                  font=('Helvetica', '12'))
        self.textLabel.pack(anchor='n', expand=True)

        self.icon_w = tk.PhotoImage(file="hakodate.png")
        self.imageLabel = tk.Label(self.frame2, image=self.icon_w)
        self.imageLabel.pack(anchor='n', expand=True)

        # フレーム1からmainフレームに戻るボタン
        self.back_button = tk.Button(self.frame2, text="NEXT", command=lambda: self.changePage(self.frame4))
        self.back_button.pack()
        # # --------------------------------------------------------------------------
        # # -----------------------------------frame3---------------------------------
        # # 移動先フレーム作成
        # self.frame3 = tk.Frame()
        # self.frame3.grid(row=0, column=0, sticky="nsew")
        # # タイトルラベル作成
        # self.titleLabel = tk.Label(self.frame3, text="Q2:再帰関数\n欠けた雪の結晶", font=('Helvetica', '24'))
        # self.titleLabel.pack(anchor='n', expand=True)
        #
        # self.textLabel = tk.Label(self.frame3, text="2つの図は雪の結晶の形で、右の図は通常のもの、左の図が欠けたものである。\n"
        #                                             "最終的なゴールは欠けた状態だが、それには通常の結晶から考えるのがよい。\n\n"
        #                                             "この結晶は中心から8方向に線が拡がっているのが基本構造である。\n"
        #                                             "図では3時から時計回り方向に順番に線を描いている。\n"
        #                                             "はじめ8方向に拡がる線の長さは100とする。\n\n"
        #                                             "それぞれの線の先端から小さくなった同じ構造が再び拡がることで結晶となる。\n"
        #                                             "図では新たに結晶を伸ばすさいには長さを40ずつ短くし、\n"
        #                                             "値が0を下回った場合には新たに結晶を拡げないようにしている。\n\n"
        #                                             "このような通常の結晶において、8本の線を描画するときに、\n"
        #                                             "8本目の線であればその線もそこから伸びる結晶も描かないことにする。\n"
        #                                             "ただし、その後に拡がる前の結晶構造に戻る場合を考えると、\n"
        #                                             "8本目の場合もカメの向きを調整する必要がある。\n", justify='left',
        #                           font=('Helvetica', '12'))
        # self.textLabel.pack(anchor='n', expand=True)
        #
        # self.icon_s1 = tk.PhotoImage(file="snow.png")
        # self.imageLabel = tk.Label(self.frame3, image=self.icon_s1)
        # self.imageLabel.pack(anchor='n', side=tk.RIGHT, padx=96)
        #
        # self.icon_s2 = tk.PhotoImage(file="sno.png")
        # self.imageLabel = tk.Label(self.frame3, image=self.icon_s2)
        # self.imageLabel.pack(anchor='ne', expand=True)
        #
        # # フレーム1からmainフレームに戻るボタン
        # self.back_button = tk.Button(self.frame3, text="NEXT", command=lambda: self.changePage(self.frame4))
        # self.back_button.pack(anchor="e", side=tk.RIGHT)
        #
        # self.back_button = tk.Button(self.frame3, text="BACK", command=lambda: self.changePage(self.frame2))
        # self.back_button.pack(anchor="w")
        # --------------------------------------------------------------------------
        # -----------------------------------frame4---------------------------------
        # 移動先フレーム作成
        self.frame4 = tk.Frame()
        self.frame4.grid(row=0, column=0, sticky="nsew")
        # タイトルラベル作成
        self.titleLabel = tk.Label(self.frame4, text="Good job.", font=('Helvetica', '35'))
        self.titleLabel.pack(anchor='n')

        self.titleLabel = tk.Label(self.frame4, text="お疲れ様でした。\n最後にENDボタンを押して終わりです。", font=('Helvetica', '24'))
        self.titleLabel.pack(anchor='center', expand=True)
        # フレーム1からmainフレームに戻るボタン
        self.back_button = tk.Button(self.frame4, text="END", command=lambda: self.destroy())
        self.back_button.pack(side=tk.RIGHT, expand=True)
        self.back_button = tk.Button(self.frame4, text="BACK", command=lambda: self.changePage(self.frame2))
        self.back_button.pack(anchor="w")
        # --------------------------------------------------------------------------

        # frame1を一番上に表示
        self.frame1.tkraise()

    def changePage(self, page):
        '''
        画面遷移用の関数
        '''
        page.tkraise()


def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    # print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
    #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
    #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    df_add = pd.DataFrame([[gaze_data['left_gaze_point_on_display_area'][0],
                            gaze_data['left_gaze_point_on_display_area'][1],
                            gaze_data['right_gaze_point_on_display_area'][0],
                            gaze_data['right_gaze_point_on_display_area'][1],
                            gaze_data['left_pupil_diameter'],
                            gaze_data['right_pupil_diameter'],
                            pyautogui.position()[0],
                            pyautogui.position()[1],
                           get_now()]],
                          columns=['Left_x', 'Left_y', 'Right_x', 'Right_y',  'left_pupil_diameter', 'right_pupil_diameter', 'mouse_x', 'mouse_y',  'time_stamp'])

    df_add.to_csv('sample_ex.csv', mode='a', header=False, index=False)
    # df = df.append(df_add, ignore_index=True)
    # print(df_add)

# tobiiとマウスのタイムスタンプ用
def get_now():
    # now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    now = datetime.now().strftime("%H:%M:%S.%f")
    return now


class Monitor:
    def __init__(self):
        self.counter = 1

    def count(self):
        self.counter += 1
        # print('Count:{0}'.format(self.counter))
        # print(get_now())

    def call(self):
        self.mouse_listener.stop() # 規定回数過ぎたら終了
        self.keyboard_listener.stop()

    # マウス入力
    def on_click(self, x, y, button, pressed):
        """クリック時に呼ばれる
        """
        # print('{0} at {1}'.format(
        #     'Pressed' if pressed else 'Released',
        #     (x,y)))
        df_click_add = pd.DataFrame([[x, y, self.counter, pressed, get_now()]], columns=['x', 'y', 'count', 'PorR', 'time_stamp'])
        df_click_add.to_csv('sample_ex_click.csv', mode='a', header=False, index=False)

        if pressed==False:
            # print("pressed")
            self.count()

    # キーボード入力
    def on_press(self, key):
        """キーを押したときに呼ばれる"""
        try:
            # print('alphanumeric key {0} pressed'.format(key.char))
            # print(get_now())
            df_keyboard_add = pd.DataFrame([[key, True, get_now()]], columns=['key', 'PorR', 'time_stamp'])
            df_keyboard_add.to_csv('sample_ex_key.csv', mode='a', header=False, index=False)

        except AttributeError:
            # print('special key {0} pressed'.format(key))
            # print(get_now())
            df_keyboard_add = pd.DataFrame([[key, True, get_now()]], columns=['key', 'PorR', 'time_stamp'])
            df_keyboard_add.to_csv('sample_ex_key.csv', mode='a', header=False, index=False)

    def on_release(self, key):
        """キーを離したときに呼ばれる"""
        try:
            # print('alphanumeric key {0} released'.format(key.char))
            # print(get_now())
            df_keyboard_add = pd.DataFrame([[key, False, get_now()]], columns=['key', 'PorR', 'time_stamp'])
            df_keyboard_add.to_csv('sample_ex_key.csv', mode='a', header=False, index=False)

        except AttributeError:
            # print('special key {0} released'.format(key))
            # print(get_now())
            df_keyboard_add = pd.DataFrame([[key, False, get_now()]], columns=['key', 'PorR', 'time_stamp'])
            df_keyboard_add.to_csv('sample_ex_key.csv', mode='a', header=False, index=False)


    def start(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()
    #     with mouse.Listener(
    #         on_click=self.on_click) as self.mouse_listener, keyboard.Listener(
    #         on_press=self.on_press, on_release=self.on_release) as self.keyboard_listener:
    #         self.mouse_listener.join()
    #         self.keyboard_listener.join()

# def GetSource():
#     file = open("test01.py", "r")
#     text = file.read()
#     file.close()
#     t = datetime.now()
#     str_t = t.strftime('%H-%M-%S')
#     new = open("sourcecodesPerSec/code" + str(str_t) + ".py", "w")
#     # new.write("# " + str(inspect.stack()[-1][1]) + "\n")
#     new.write("# " + str(datetime.now()) + "\n")
#     new.write(text)
#     new.close()
#
# def scheduler(interval, f, wait = True):
#     base_time = time.time()
#     next_time = 0
#     while True:
#         t = threading.Thread(target=f)
#         t.start()
#         if wait:
#             t.join()
#         next_time = ((base_time - time.time()) % interval) or interval
#         time.sleep(next_time)
def scheduler():
    t = threading.Timer(5, scheduler)
    t.start()
    file = open("test01.py", "r")
    text = file.read()
    file.close()
    t = datetime.now()
    str_t = t.strftime('%H-%M-%S-%f')
    new = open("sourcecodesPerSec/code" + str(str_t) + ".py", "w")
    # new.write("# " + str(inspect.stack()[-1][1]) + "\n")
    new.write("# " + str(datetime.now()) + "\n")
    new.write(text)
    new.close()

if __name__ == "__main__":
    found_eyetrackers = tr.find_all_eyetrackers()
    my_eyetracker = found_eyetrackers[0]
    print("Address: " + my_eyetracker.address)
    print("Model: " + my_eyetracker.model)
    print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
    print("Serial number: " + my_eyetracker.serial_number)
    # df = pd.DataFrame(columns=['Left_x', 'Left_y', 'Right_x', 'Right_y', 'mouse_x', 'mouse_y', 'time_stamp'])
    df = pd.DataFrame(columns=['Left_x', 'Left_y', 'Right_x', 'Right_y', 'left_pupil_diameter', 'right_pupil_diameter', 'mouse_x', 'mouse_y', 'time_stamp'])
    df.to_csv('sample_ex.csv', mode='w', index=False)
    df_click = pd.DataFrame(columns=['x', 'y', 'count', 'PorR', 'time_stamp'])
    df_click.to_csv('sample_ex_click.csv', mode='w', index=False)
    df_keyboard = pd.DataFrame(columns=['key', 'PorR', 'time_stamp'])
    df_keyboard.to_csv('sample_ex_key.csv', mode='w', index=False)
    my_eyetracker.retrieve_calibration_data()

    # os.makedirs("screenshot_ex", exist_ok=True)

    my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    monitor = Monitor()
    monitor.start()
    print("monimoni")

    t1 = threading.Thread(target = scheduler)
    t1.setDaemon(True)
    t1.start()

    app = App()
    app.mainloop()
    monitor.call()

    print("nice boat")
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)


