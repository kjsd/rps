# ==============================================================================
# 🎓 プログラミング教室用：AIじゃんけん 模範解答・完成版 (先生用 / デモ用)
# ==============================================================================
# 【模範解答】
# ・【ミッション 1】じゃんけん勝敗判定ルール（judge）
# ・【ミッション 2】相手の最多手を読んで裏をかく「最頻手カウンターAI」（choose_ai_hand）
# が完全に実装されています。
# ==============================================================================

from mblock import event
import random


# ==============================================================================
# 🛑【ゾーン A】触ってはいけないシステム領域（ルール定数）
# ==============================================================================
ROCK = 1      # グー ✊
SCISSORS = 2  # チョキ ✌️
PAPER = 3     # パー ✋

DRAW = 0  # あいこ
WIN = 1   # あなたの勝ち
LOSE = 2  # AIの勝ち


# ==============================================================================
# 🟢【ゾーン B】生徒さんのワークスペース ★模範解答実装エリア
# ==============================================================================

class JankenBrain:
    """
    じゃんけんの「ルール」と「AIの頭脳」を決めるクラスです。
    """

    # --------------------------------------------------------------------------
    # 🎯【ミッション 1 模範解答】じゃんけんの勝敗判定
    # --------------------------------------------------------------------------
    def judge(self, player_hand, ai_hand):
        """プレイヤーの手とAIの手を比べて、勝敗を判定する"""
        if player_hand == ai_hand:
            return DRAW

        if (player_hand == ROCK and ai_hand == SCISSORS) or \
           (player_hand == SCISSORS and ai_hand == PAPER) or \
           (player_hand == PAPER and ai_hand == ROCK):
            return WIN
        else:
            return LOSE

    # --------------------------------------------------------------------------
    # 🎯【ミッション 2 模範解答】相手の癖を読む「最頻手カウンターAI」
    # --------------------------------------------------------------------------
    def choose_ai_hand(self, round_no, count_rock, count_scissors, count_paper):
        """
        相手が一番多く出している手を調べ、その手に勝つ手を出す！
        ※ mBlockの仕様に配慮し、forループを使わずに if/elif で安全に比較します。
        """
        # 1〜2回戦はデータが少ないため、ランダムに出して様子を見る
        if round_no <= 2:
            return random.choice([ROCK, SCISSORS, PAPER])

        # 相手が一番多く出している手を調べる
        most_player_hand = ROCK
        max_count = count_rock

        if count_scissors > max_count:
            most_player_hand = SCISSORS
            max_count = count_scissors

        if count_paper > max_count:
            most_player_hand = PAPER

        # 相手の最多の手「に勝つ手」を返す！
        if most_player_hand == ROCK:
            return PAPER     # グーにはパーで勝つ！
        elif most_player_hand == SCISSORS:
            return ROCK      # チョキにはグーで勝つ！
        else:
            return SCISSORS  # パーにはチョキで勝つ！


# ==============================================================================
# 🛑【ゾーン C】触ってはいけないシステム領域（ゲーム進行 & スプライト演出）
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
        # 1. AIの手を決定（JankenBrainに相談）
        ai_hand = self.brain.choose_ai_hand(
            self.round_no,
            self.count_rock,
            self.count_scissors,
            self.count_paper
        )

        # 2. 勝敗判定（JankenBrainに相談）
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
            str(total) + "戦: " + str(self.wins) + "勝 " + str(self.losses) + "敗 " + str(self.draws) + "分け\n\n" +
            "📊 AI分析: あなたの最多の手は「" + most_name + "」でした！\n" +
            "🚩 緑の旗でまた最初から対戦できるよ！"
        )


# ゲーム管理インスタンスの生成
game = GameDirector()


# ==============================================================================
# ⚡ イベントハンドラ（緑の旗 & キーボード操作）
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
