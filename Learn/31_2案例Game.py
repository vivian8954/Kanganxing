"""
1.设计一个Game类（类名）
2.属性：
定义一个top_score类属性->记录游戏的历史最高分
定义一个player_name实例属性->记录当前游戏的玩家姓名
3. 方法：
静态方法show_help）->直接打印这是游戏帮助信息
类方法 show_top_score(）->显示历史最高分
实例方法start_game(）->开始当前玩家的游戏
3.1输出玩家xxx开始游戏
3.2使用随机数，生成10－100之间的随机数字作为本次游戏的得分
3.3打印玩家xxx本次游戏得分xxx
3.4判断本次游戏得分和最高分之间的关系
4．主程序步骤：_main
1查看帮助信息
2查看历史最高分
3创建游戏对象，开始游戏
"""
class Game:
    top_score = 0
    def __init__(self, player_name):
        self.player_name = player_name

    @staticmethod
    def show_help():
        print("这是游戏帮助信息")

    @classmethod
    def show_top_score(cls):
        #打印历史最高分
        print( "历史最高分是：", cls.top_score)

    def start_game(self):
        print(self.player_name, "开始游戏")
        import random
        score = random.randint(10, 100)
        print(self.player_name, "本次游戏得分", score)
        if score > Game.top_score:
            Game.top_score = score
if __name__ == '__main__':
    Game.show_help()
    Game.show_top_score()
    player1 = Game("张三")
    player1.start_game()
    player2 = Game("李四")
    player2.show_top_score()
    player2.start_game()
    player2.show_top_score()
    player2.start_game()
    player2.show_top_score()