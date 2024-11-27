from wifi import Cell, Scheme

# 사용 가능한 모든 와이파이 네트워크 스캔
print(Cell.all("wlan0").__next__().signal)

# for n in network:
#     print(n.signal)
