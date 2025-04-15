import pyperclip
import sys

if sys.argv[1] == 'ja':
    head = '''<div class="table_wrapper">
<table>
<tr>
<th>番号</th>
<th>深さ</th>
<th>最善手</th>
<th>評価値</th>
<th>時間(秒)</th>
<th>ノード数</th>
<th>NPS</th>
</tr>
'''
else:
    head = '''<div class="table_wrapper">
<table>
<tr>
<th>No.</th>
<th>Depth</th>
<th>Best Move</th>
<th>Score</th>
<th>Time (sec)</th>
<th>Nodes</th>
<th>NPS</th>
</tr>
'''

'''
#5.4.0
idxes = [0, 3, 13, 15, 6, 17, 19]
need_coord_translate = 13
'''
'''
#5.5.0
idxes = [0, 2, 6, 4, 11, 8, 16]
need_coord_translate = -1
'''
'''
#5.7.0-6.0.0
idxes = [0, 2, 6, 4, 10, 8, 12]
need_coord_translate = -1
'''
#6.1.0-
idxes = [0, 2, 3, 4, 5, 6, 7]
need_coord_translate = -1

def coord_translator(cell):
    cell = 63 - int(cell)
    y = cell // 8
    x = cell % 8
    return chr(ord('a') + x) + str(y + 1)

whole_time = 0
whole_nodes = 0
res = head
while True:
    data = input().replace('|', ' ').split()
    print(data)
    try:
        use_data = []
        for idx in idxes:
            if idx == need_coord_translate:
                use_data.append(coord_translator(data[idx]))
            else:
                if idx == idxes[4]:
                    tims = data[idx].split(':')
                    tim_float = float(tims[0]) * 3600 + float(tims[1]) * 60 + float(tims[2])
                    tim = str(tim_float)
                    #tim = str(round(int(data[idx]) / 1000, 3))
                    use_data.append(tim)
                    whole_time += tim_float
                else:
                    if idx == idxes[1]:
                        data[idx] = data[idx].replace('@100%', '')
                    use_data.append(data[idx])
                if idx == idxes[5]:
                    whole_nodes += int(data[idx])
        res += '<tr>\n'
        for use_datum in use_data:
            res += '<td>'
            res += use_datum
            res += '</td>\n'
        res += '</tr>\n'
    except:
        break
if sys.argv[1] == 'ja':
    res += '''<tr>
<td>全体</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>''' + str(round(whole_time, 3)) + '''</td>
<td>''' + str(whole_nodes) + '''</td>
<td>''' + str(round(whole_nodes / whole_time)) + '''</td>
</tr>
'''
else:
    res += '''<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>''' + str(round(whole_time, 3)) + '''</td>
<td>''' + str(whole_nodes) + '''</td>
<td>''' + str(round(whole_nodes / whole_time)) + '''</td>
</tr>
'''
res += '''</table>
</div>'''

#print(res)

pyperclip.copy(res)