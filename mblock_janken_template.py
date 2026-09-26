# ==============================================================================
# 🎓 プログラミング教室用：AIじゃんけん ワークシート (生徒さん配布用)
# ==============================================================================
# 【生徒さんへ】
# このプログラムは、パンダとじゃんけんバトルをするAIゲームです！
#
# 🔰 このファイルには「さわってはいけない部分」と「みんなが改造する部分」があります。
#    緑色の枠で囲まれた【ミッション1】と【ミッション2】だけを書き換えて、
#    世界でひとつだけの最強じゃんけんAIを作ってみよう！
# ==============================================================================

from mblock import event
import random


# ==============================================================================
# 🛑【ゾーン A】触ってはいけないシステム領域（ルール定数）
# ※ ここは変更しないでね！
# ==============================================================================
ROCK = 1      # グー ✊
SCISSORS = 2  # チョキ ✌️
PAPER = 3     # パー ✋

DRAW = 0  # あいこ
WIN = 1   # あなたの勝ち
LOSE = 2  # AIの勝ち


# ==============================================================================
# 🟢【ゾーン B】生徒さんのワークスペース ★ここを自由にプログラミングしよう！
# ==============================================================================

class JankenBrain:
    """
    じゃんけんの「ルール」と「AIの頭脳」を決めるクラスです。
    みんなには、この中にある 2 つの関数を作ってもらいます！
    """

    # --------------------------------------------------------------------------
    # 🎯【ミッション 1】じゃんけんの勝敗を判定しよう！
    # --------------------------------------------------------------------------
    def judge(self, player_hand, ai_hand):
        """
        プレイヤーの手とAIの手を比べて、勝敗を判定する関数です。
        
        【入力される値】
          - player_hand: あなたが出した手（ROCK, SCISSORS, PAPER のどれか）
          - ai_hand: AIが出した手（ROCK, SCISSORS, PAPER のどれか）
          
        【返す値（returnする値）】
          - DRAW (0): あいこ
          - WIN  (1): あなたの勝ち
          - LOSE (2): あなたの負け
        """
        # --- ヒント ---
        # 1. 2人の手が同じなら？ -> return DRAW
        # 2. あなたが勝つパターン:
        #    - あなたがグー(ROCK) かつ AIがチョキ(SCISSORS)
        #    - あなたがチョキ(SCISSORS) かつ AIがパー(PAPER)
        #    - あなたがパー(PAPER) かつ AIがグー(ROCK)
        # 3. それ以外は？ -> return LOSE
        # -------------

        # TODO: ここに勝敗判定のコードを書こう！
        if player_hand == ai_hand:
            return DRAW

        if (player_hand == ROCK and ai_hand == SCISSORS) or \
           (player_hand == SCISSORS and ai_hand == PAPER) or \
           (player_hand == PAPER and ai_hand == ROCK):
            return WIN
        else:
            return LOSE


    # --------------------------------------------------------------------------
    # 🎯【ミッション 2】相手の癖を読む「AIの頭脳」を育てよう！
    # --------------------------------------------------------------------------
    def choose_ai_hand(self, round_no, count_rock, count_scissors, count_paper):
        """
        AIが次に出す手を決める関数です。
        
        【もらえる情報】
          - round_no: いま何回戦目か（1〜5）
          - count_rock: 相手がこれまでに「グー」を出した回数
          - count_scissors: 相手がこれまでに「チョキ」を出した回数
          - count_paper: 相手がこれまでに「パー」を出した回数
          
        【返す値（returnする値）】
          - AIが出す手（ROCK, SCISSORS, PAPER のどれか）
        """
        # ======================================================================
        # 💡 AI進化のステップ（好きなレベルに挑戦してね！）
        #
        # 【レベル 1: 初心者AI】
        # まずはランダムに手を出してみよう！
        # return random.choice([ROCK, SCISSORS, PAPER])
        #
        # 【レベル 2: 観察AI（相手の癖を読む！）】
        # 相手が過去に一番多く出している手を調べて、その手に勝つ手を出そう！
        #   ・相手がグーを多く出しているなら？ -> パー(PAPER)を出す！
        #   ・相手がチョキを多く出しているなら？ -> グー(ROCK)を出す！
        #   ・相手がパーを多く出しているなら？ -> チョキ(SCISSORS)を出す！
        #
        # ⚠️ 注意: mBlockの仕様上、関数の中に「for」や「while」を書くと
        #    動かなくなってしまうので、「if / elif」を使って作ってね！
        # ======================================================================

        # TODO: ここにAIの思考コードを書こう！（初期状態はレベル1のランダム思考です）
        return random.choice([ROCK, SCISSORS, PAPER])


# ==============================================================================
# 🛑【ゾーン C】触ってはいけないシステム領域（ゲーム進行 & スプライト演出）
# ※ ここから下のコードは絶対にいじらないでね！
# ==============================================================================

class GameDirector:
    """ゲーム全体の進行管理を行う司令塔"""
    def __init__(self):
        self.brain = JankenBrain()
        self.round_no = 1
        self.max_rounds = 5

        self.wins = 0
        self.losses = 0
        self.draws = 0

        self.count_rock = 0
        self.count_scissors = 0
        self.count_paper = 0

    def start_game(self):
        self.round_no = 1
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.count_rock = 0
        self.count_scissors = 0
        self.count_paper = 0
        return "AIじゃんけんバトル開始！\n[1]:グー [2]:チョキ [3]:パー を押してね！"

    def get_hand_name(self, hand):
        if hand == ROCK:
            return "グー ✊"
        elif hand == SCISSORS:
            return "チョキ ✌️"
        elif hand == PAPER:
            return "パー ✋"
        return "不明"

    def get_result_name(self, result):
        if result == DRAW:
            return "あいこ！"
        elif result == WIN:
            return "あなたの勝ち！🎉"
        elif result == LOSE:
            return "AIの勝ち！🤖"
        return ""

    def play_round(self, player_hand):
        # 1. AIの手を決定（生徒さんの作った頭脳に相談）
        ai_hand = self.brain.choose_ai_hand(
            self.round_no,
            self.count_rock,
            self.count_scissors,
            self.count_paper
        )

        # 2. 勝敗判定（生徒さんの作った審判に相談）
        result = self.brain.judge(player_hand, ai_hand)

        # 3. 成績集計
        if result == WIN:
            self.wins += 1
        elif result == LOSE:
            self.losses += 1
        else:
            self.draws += 1

        if player_hand == ROCK:
            self.count_rock += 1
        elif player_hand == SCISSORS:
            self.count_scissors += 1
        elif player_hand == PAPER:
            self.count_paper += 1

        # 4. メッセージ作成
        p_name = self.get_hand_name(player_hand)
        ai_name = self.get_hand_name(ai_hand)
        res_name = self.get_result_name(result)

        round_msg = (
            "【第 " + str(self.round_no) + " 回戦 結果】\n" +
            "あなた: " + p_name + "\n" +
            "AIの手: " + ai_name + "\n" +
            "判定: " + res_name
        )

        self.round_no += 1
        if self.round_no <= self.max_rounds:
            return round_msg + "\n\n👉 第 " + str(self.round_no) + " 回戦！手を押してね！"
        else:
            summary = self.get_summary()
            return round_msg + "\n\n" + summary

    def get_summary(self):
        most_name = "グー ✊"
        max_c = self.count_rock
        if self.count_scissors > max_c:
            most_name = "チョキ ✌️"
            max_c = self.count_scissors
        if self.count_paper > max_c:
            most_name = "パー ✋"

        total = self.wins + self.losses + self.draws
        return (
            "🏆 【対戦終了！】 🏆\n" +
            str(total) + "戦: " + str(self.wins) + "勝 " + str(self.losses) + "敗 " + str(self.draws) + "分け\n" +
            "📊 AI分析: あなたの最多の手は「" + most_name + "」でした！\n" +
            "🚩 緑の旗でまた最初から対戦できるよ！"
        )


# ゲーム管理インスタンスの生成
game = GameDirector()


# ==============================================================================
# ⚡ イベントハンドラ（緑の旗 & キーボード操作）
# ※ ここも変更しないでね！
# ==============================================================================
@event.greenflag
def on_greenflag():
    try:
        msg = game.start_game()
        sprite.say(msg)
    except Exception as e:
        print("エラー: " + str(e))

@event.keypressed("1")
def on_key_1():
    try:
        msg = game.play_round(ROCK)
        sprite.say(msg)
    except Exception as e:
        print("エラー: " + str(e))

@event.keypressed("2")
def on_key_2():
    try:
        msg = game.play_round(SCISSORS)
        sprite.say(msg)
    except Exception as e:
        print("エラー: " + str(e))

@event.keypressed("3")
def on_key_3():
    try:
        msg = game.play_round(PAPER)
        sprite.say(msg)
    except Exception as e:
        print("エラー: " + str(e))

print("--- [AIじゃんけんシステム 準備完了！緑の旗を押してスタート] ---")
