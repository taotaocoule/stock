# 日报
# 板块情况
# 资金情况
# 指数情况

import sys
sys.path.append("../")

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
import spider.data.market as market
import spider.data.board as board

board_data=board.Board().board().apply(pd.to_numeric,errors='ignore').sort_values('涨跌幅')

# 板块总体涨跌情况
def board_all():
	plt.subplot(3,1,1)
	sns.barplot(board_data['板块名称'],board_data['涨跌幅'])
	plt.title('涨跌幅')
	plt.xlabel("")
	plt.ylabel("")
	plt.xticks([])
	plt.subplot(3,1,2)
	sns.barplot(board_data['板块名称'],board_data['换手率'])
	plt.xticks([])
	plt.xlabel("")
	plt.ylabel("")
	plt.title('换手率')
	plt.subplot(3,1,3)
	sns.barplot(board_data['板块名称'],board_data['总市值'])
	plt.xticks([])
	plt.ylabel("")
	plt.xlabel("")
	plt.title('总市值')
	plt.savefig("板块总体.jpg")