import subprocess
from othello_py import *
import sys
from random import shuffle
from time import time
import datetime

d_today = str(datetime.date.today())
t_now = str(datetime.datetime.now().time())

'''
# special
with open('problem/r18_difficult1_board.txt', 'r') as f:
    tactic = [elem for elem in f.read().splitlines()]
whole_log_file = 'egaroucid_vs_edax_time_log/' + 'log_' + d_today.replace('-', '') + '_' + t_now.split('.')[0].replace(':', '') + '_board_special_' + 'whole' + '.txt'
logfile_format = 'egaroucid_vs_edax_time_log/' + 'log_' + d_today.replace('-', '') + '_' + t_now.split('.')[0].replace(':', '') + '_board_special_'
GAME_OFFSET = 0
#'''

#'''
# difficult
with open('problem/random18_boards/difficult.txt', 'r') as f:
    tactic = [elem for elem in f.read().splitlines()]
whole_log_file = 'egaroucid_vs_edax_time_log/' + 'log_' + d_today.replace('-', '') + '_' + t_now.split('.')[0].replace(':', '') + '_board_difficult_' + 'whole' + '.txt'
logfile_format = 'egaroucid_vs_edax_time_log/' + 'log_' + d_today.replace('-', '') + '_' + t_now.split('.')[0].replace(':', '') + '_board_difficult_'
GAME_OFFSET = 1
#'''

'''
# default
with open('problem/random18_boards/0000000.txt', 'r') as f:
    tactic = [elem for elem in f.read().splitlines()]
whole_log_file = 'egaroucid_vs_edax_time_log/' + 'log_' + d_today.replace('-', '') + '_' + t_now.split('.')[0].replace(':', '') + '_board_' + 'whole' + '.txt'
logfile_format = 'egaroucid_vs_edax_time_log/' + 'log_' + d_today.replace('-', '') + '_' + t_now.split('.')[0].replace(':', '') + '_board_'
GAME_OFFSET = 78
#'''

print(len(tactic), 'openings found', file=sys.stderr)

time_limit = int(sys.argv[1])
n_games = int(sys.argv[2])

file = None
egaroucid_cmd = 'versions/Egaroucid_for_Console_beta/Egaroucid_for_console_clang.exe -quiet -noise -nobook -ponder -t 8 -hash 30 -time ' + str(time_limit)
if len(sys.argv) == 4:
    file = sys.argv[3]
    print('egaroucid eval ', file, file=sys.stderr)
    egaroucid_cmd += ' -eval ' + file

print(egaroucid_cmd, file=sys.stderr)

egaroucid_win = [0, 0]
edax_win = [0, 0]
draw = [0, 0]
egaroucid_disc_diff_sum = 0
egaroucid_n_played = 0

print('time_limit', time_limit, file=sys.stderr)
print('openings', len(tactic), file=sys.stderr)

max_num = min(len(tactic), n_games)
smpl = range(len(tactic))
print('play', max_num, 'games', file=sys.stderr)


#edax_cmd = 'versions/edax_4_4/edax-4.4 -q -l 50 -ponder on -n 8 -game-time ' + str(time_limit)
edax_cmd = 'versions/edax_4_5_2/wEdax-x64-modern.exe -q -l 50 -ponder on -n 8 -h 30 -game-time ' + str(time_limit)


def write_log(*args, end='\n', sep=' '):
    s = sep.join([str(elem) for elem in args])
    s += end
    with open(whole_log_file, 'a') as f:
        f.write(s)

for num in range(GAME_OFFSET, max_num + GAME_OFFSET):
    tactic_idx = smpl[num % len(tactic)]
    for player in [black, white]:
        #for player in [white, black]:
        logfile = logfile_format + str(num) + '_' + str(player) + '.txt'
        egaroucid_cmd_log = egaroucid_cmd + ' -logfile ' + logfile
        egaroucid = subprocess.Popen(egaroucid_cmd_log.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        edax = subprocess.Popen(edax_cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print('')
        write_log('')
        print('player', player)
        if player == 0:
            print('Egaroucid plays black')
            write_log('Egaroucid plays black')
        else:
            print('Egaroucid plays white')
            write_log('Egaroucid plays white')
        record = ''
        boards = []
        o = othello()
        egaroucid_used_time = 0
        edax_used_time = 0
        o.n_stones[black] = 0
        o.n_stones[white] = 0
        for yy in range(8):
            for xx in range(8):
                coord = yy * 8 + xx
                if tactic[tactic_idx][coord] == 'X':
                    o.grid[yy][xx] = black
                    o.n_stones[black] += 1
                elif tactic[tactic_idx][coord] == 'O':
                    o.grid[yy][xx] = white
                    o.n_stones[white] += 1
        o.player = black if tactic[tactic_idx][65] == 'X' else white
        grid_str = 'setboard ' + tactic[tactic_idx] + '\n'
        egaroucid.stdin.write(grid_str.encode('utf-8'))
        egaroucid.stdin.flush()
        edax.stdin.write(grid_str.encode('utf-8'))
        edax.stdin.flush()
        egaroucid.stdin.write(('mode ' + str(1 - player) + '\n').encode('utf-8'))
        egaroucid.stdin.flush()
        edax.stdin.write(('mode ' + str(player) + '\n').encode('utf-8'))
        edax.stdin.flush()
        print(tactic[tactic_idx])
        write_log(tactic[tactic_idx])
        while True:
            if not o.check_legal():
                o.player = 1 - o.player
                if o.check_legal():
                    if o.player == 1 - player: # edax -> (pass) -> edax
                        edax.stdin.write('ps\n'.encode('utf-8'))
                        edax.stdin.flush()
                else:
                    break
            move_strt_time = time()
            if o.player == player:
                #egaroucid.stdin.write('go\n'.encode('utf-8'))
                #egaroucid.stdin.flush()
                line = ''
                while line == '':
                    line = egaroucid.stdout.readline().decode().replace('\r', '').replace('\n', '')
                coord = line
                try:
                    y = int(coord[1]) - 1
                    x = ord(coord[0]) - ord('a')
                except:
                    print('')
                    print('error')
                    o.print_info()
                    print(o.player, player)
                    print(line)
                    print(coord)
                    egaroucid.stdin.write('quit\n'.encode('utf-8'))
                    egaroucid.stdin.flush()
                    edax.stdin.write('quit\n'.encode('utf-8'))
                    edax.stdin.flush()
                    exit()
                play_cmd ='play ' + coord + '\n'
                egaroucid_used_time += time() - move_strt_time
                edax.stdin.write(play_cmd.encode('utf-8'))
                edax.stdin.flush()
            else:
                #edax.stdin.write('go\n'.encode('utf-8'))
                #edax.stdin.flush()
                while True:
                    line = ''
                    while len(line) < 3:
                        line = edax.stdout.readline().decode().replace('\r', '').replace('\n', '')
                    try:
                        coord = line.split()[2]
                        if coord != 'STILL' and coord != 'ALREADY' and coord != 'PS':
                            y = int(coord[1]) - 1
                            x = ord(coord[0]) - ord('A')
                            break
                    except:
                        print('')
                        print('error')
                        o.print_info()
                        print(o.player, player)
                        print(line)
                        print(coord)
                        egaroucid.stdin.write('quit\n'.encode('utf-8'))
                        egaroucid.stdin.flush()
                        edax.stdin.write('quit\n'.encode('utf-8'))
                        edax.stdin.flush()
                        exit()
                play_cmd ='play ' + coord + '\n'
                edax_used_time += time() - move_strt_time
                egaroucid.stdin.write(play_cmd.encode('utf-8'))
                egaroucid.stdin.flush()
            record += chr(ord('a') + x) + str(y + 1)
            print('\r' + record, end='')
            write_log(chr(ord('a') + x) + str(y + 1), end='')
            if not o.move(y, x):
                print('')
                print(o.player == player)
                o.print_info()
                print(o.player, player)
                print(coord)
                print(y, x)
        if o.n_stones[player] > o.n_stones[1 - player]:
            egaroucid_win[player] += 1
        elif o.n_stones[player] == o.n_stones[1 - player]:
            draw[player] += 1
        else:
            edax_win[player] += 1
        egaroucid_disc_diff = o.n_stones[player] - o.n_stones[1 - player]
        n_empties = 64 - (o.n_stones[player] + o.n_stones[1 - player])
        if o.n_stones[player] > o.n_stones[1 - player]:
            egaroucid_disc_diff += n_empties
        elif o.n_stones[player] < o.n_stones[1 - player]:
            egaroucid_disc_diff -= n_empties
        egaroucid_disc_diff_sum += egaroucid_disc_diff
        egaroucid_n_played += 1
        egaroucid.kill()
        edax.kill()
        print('')
        print('eg', egaroucid_disc_diff, str(o.n_stones[black]) + '-' + str(o.n_stones[white]))
        print('egaroucid', egaroucid_used_time, 's', 'edax', edax_used_time, 's')
        print(num, max_num, ' ', egaroucid_win, draw, edax_win, sum(egaroucid_win) + sum(draw) * 0.5, sum(edax_win) + sum(draw) * 0.5, 
              round((sum(egaroucid_win) + sum(draw) * 0.5) / max(1, sum(egaroucid_win) + sum(edax_win) + sum(draw)), 6), 
              round(egaroucid_disc_diff_sum / egaroucid_n_played, 6))
        write_log('')
        write_log('eg', egaroucid_disc_diff, str(o.n_stones[black]) + '-' + str(o.n_stones[white]))
        write_log('egaroucid', egaroucid_used_time, 's', 'edax', edax_used_time, 's')
        write_log(num, max_num, ' ', egaroucid_win, draw, edax_win, sum(egaroucid_win) + sum(draw) * 0.5, sum(edax_win) + sum(draw) * 0.5, 
              round((sum(egaroucid_win) + sum(draw) * 0.5) / max(1, sum(egaroucid_win) + sum(edax_win) + sum(draw)), 6), 
              round(egaroucid_disc_diff_sum / egaroucid_n_played, 6))

print('', file=sys.stderr)
print('time_limit: ', time_limit, 
      ' Egaroucid plays black WDL: ', egaroucid_win[0], '-', draw[0], '-', edax_win[0], ' ', (egaroucid_win[0] + draw[0] * 0.5) / (egaroucid_win[0] + edax_win[0] + draw[0]), 
      ' Egaroucid plays white WDL: ', egaroucid_win[1], '-', draw[1], '-', edax_win[1], ' ', (egaroucid_win[1] + draw[1] * 0.5) / (egaroucid_win[1] + edax_win[1] + draw[1]), 
      ' Egaroucid win rate: ', round((sum(egaroucid_win) + sum(draw) * 0.5) / max(1, sum(egaroucid_win) + sum(edax_win) + sum(draw)), 6), 
      ' Egaroucid average discs earned: ', round(egaroucid_disc_diff_sum / egaroucid_n_played, 6), 
      sep='')

write_log('time_limit: ', time_limit, 
      ' Egaroucid plays black WDL: ', egaroucid_win[0], '-', draw[0], '-', edax_win[0], ' ', (egaroucid_win[0] + draw[0] * 0.5) / (egaroucid_win[0] + edax_win[0] + draw[0]), 
      ' Egaroucid plays white WDL: ', egaroucid_win[1], '-', draw[1], '-', edax_win[1], ' ', (egaroucid_win[1] + draw[1] * 0.5) / (egaroucid_win[1] + edax_win[1] + draw[1]), 
      ' Egaroucid win rate: ', round((sum(egaroucid_win) + sum(draw) * 0.5) / max(1, sum(egaroucid_win) + sum(edax_win) + sum(draw)), 6), 
      ' Egaroucid average discs earned: ', round(egaroucid_disc_diff_sum / egaroucid_n_played, 6), 
      sep='')