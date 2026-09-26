# ==============================================================================
# 🧪 mBlock 5 スプライト Python じゃんけん (完全同期版 test_mblock.py)
# ==============================================================================
# 【真犯人：forループによるジェネレータ化の完全回避】
# mBlock は for ループがある関数を勝手にジェネレータに変換してしまうため、
# 毎ラウンドその場で集計カウントを更新し、for ループを完全撤廃しました！
# これにより、すべての関数が確実に純粋な値（数値・文字列）を返します！
# ==============================================================================

from mblock import event
import random

print("--- [スクリプト読み込み開始] ---")


class TestDirector:
    """じゃんけんのロジック・審判・AI頭脳を担当するモデルクラス"""
    def __init__(self):
        print("✅ [Init]: TestDirector 生成完了！")
        self.round_no = 1
        self.max_rounds = 5

        # 対戦成績カウント（forループを使わず毎ターン更新）
        self.wins = 0
        self.losses = 0
        self.draws = 0

        # 相手の手のカウント（AI分析用）
        self.count_rock = 0
        self.count_scissors = 0
        self.count_paper = 0

    def start_game(self):
        """ゲーム開始処理"""
        print("🎮 [Logic]: start_game() 実行！")
        self.round_no = 1
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.count_rock = 0
        self.count_scissors = 0
        self.count_paper = 0
        return "AIじゃんけんバトル開始！\n[1]:グー [2]:チョキ [3]:パー を押してね！"

    def get_hand_name(self, hand):
        if hand == 1:
            return "グー ✊"
        elif hand == 2:
            return "チョキ ✌️"
        elif hand == 3:
            return "パー ✋"
        return "不明"

    def get_result_name(self, result):
        if result == 0:
            return "あいこ！"
        elif result == 1:
            return "あなたの勝ち！🎉"
        elif result == 2:
            return "AIの勝ち！🤖"
        return ""

    def choose_ai_hand(self):
        """相手の癖を読むAI思考（forループなし・完全同期関数）"""
        # 1〜2回戦はランダム
        if self.round_no <= 2:
            return random.choice([1, 2, 3])

        # 相手の過去の最多の手を判定
        most_p_hand = 1
        max_c = self.count_rock

        if self.count_scissors > max_c:
            most_p_hand = 2
            max_c = self.count_scissors

        if self.count_paper > max_c:
            most_p_hand = 3

        # 相手の最多の手に勝つ手を返す (1:グー->3:パー, 2:チョキ->1:グー, 3:パー->2:チョキ)
        if most_p_hand == 1:
            return 3
        elif most_p_hand == 2:
            return 1
        else:
            return 2

    def judge(self, p, ai):
        """勝敗判定 (0:あいこ, 1:勝ち, 2:負け)"""
        if p == ai:
            return 0
        if (p == 1 and ai == 2) or (p == 2 and ai == 3) or (p == 3 and ai == 1):
            return 1
        return 2

    def play_round(self, p_hand):
        """1回戦を実行し、結果のメッセージ文字列を返す"""
        print("🎮 [Logic]: play_round(" + str(p_hand) + ") 実行！")

        # 1. AIの手を決定
        ai_hand = self.choose_ai_hand()

        # 2. 勝敗判定
        result = self.judge(p_hand, ai_hand)

        # 3. 成績と手のカウントをその場で即座に更新！（forループ不要）
        if result == 1:
            self.wins += 1
        elif result == 2:
            self.losses += 1
        else:
            self.draws += 1

        if p_hand == 1:
            self.count_rock += 1
        elif p_hand == 2:
            self.count_scissors += 1
        elif p_hand == 3:
            self.count_paper += 1

        # 4. メッセージ作成
        p_name = self.get_hand_name(p_hand)
        ai_name = self.get_hand_name(ai_hand)
        res_name = self.get_result_name(result)

        round_msg = (
            "【第 " + str(self.round_no) + " 回戦 結果】\n" +
            "あなた: " + p_name + "\n" +
            "AIの手: " + ai_name + "\n" +
            "判定: " + res_name
        )

        # 5. 次のラウンドへ進むか、終了レポートを付加して返す
        self.round_no += 1
        if self.round_no <= self.max_rounds:
            next_msg = round_msg + "\n\n👉 第 " + str(self.round_no) + " 回戦！手を押してね！"
            return next_msg
        else:
            summary = self.get_summary()
            return round_msg + "\n\n" + summary

    def get_summary(self):
        """全対戦レポートの文字列を生成して返す（forループなし）"""
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


# インスタンス生成
test_game = TestDirector()


# ==============================================================================
# イベントハンドラ（UI表示とイベントディスパッチを担当するコントローラー）
# ==============================================================================
@event.greenflag
def on_greenflag():
    print("🚩 [Event]: 緑の旗がクリックされました！")
    try:
        msg = test_game.start_game()
        print("📢 パンダ発話:\n" + msg)
        sprite.say(msg)
    except Exception as e:
        print("❌ [Error in on_greenflag]: " + str(e))

@event.keypressed("1")
def on_key_1():
    print("🎹 [Key]: 1 (グー)")
    try:
        msg = test_game.play_round(1)
        print("📢 パンダ発話:\n" + msg)
        sprite.say(msg)
    except Exception as e:
        print("❌ [Error in on_key_1]: " + str(e))

@event.keypressed("2")
def on_key_2():
    print("🎹 [Key]: 2 (チョキ)")
    try:
        msg = test_game.play_round(2)
        print("📢 パンダ発話:\n" + msg)
        sprite.say(msg)
    except Exception as e:
        print("❌ [Error in on_key_2]: " + str(e))

@event.keypressed("3")
def on_key_3():
    print("🎹 [Key]: 3 (パー)")
    try:
        msg = test_game.play_round(3)
        print("📢 パンダ発話:\n" + msg)
        sprite.say(msg)
    except Exception as e:
        print("❌ [Error in on_key_3]: " + str(e))

print("--- [スクリプト準備完了！緑の旗を押してね] ---")
