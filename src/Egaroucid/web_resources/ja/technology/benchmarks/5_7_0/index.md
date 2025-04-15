# Egaroucid 5.7.0 ベンチマーク

## The FFO endgame test suite

<a href="http://radagast.se/othello/ffotest.html" target="_blank" el=”noopener noreferrer”>The FFO endgame test suite</a>はオセロAIの終盤探索力の指標として広く使われるベンチマークです。各テストケースを完全読みし、最善手を計算します。探索時間と訪問ノード数を指標に性能を評価します。NPSはNodes Per Secondの略で、1秒あたりの訪問ノード数を表します。

使用CPUはCore i9-11900Kです。

<table>
<tr>
<th>番号</th>
<th>深さ</th>
<th>最善手</th>
<th>手番の評価値</th>
<th>探索時間(秒)</th>
<th>訪問ノード数</th>
<th>NPS</th>
</tr>
<tr>
<td>#40</td>
<td>20</td>
<td>a2</td>
<td>38</td>
<td>0.187</td>
<td>32617519</td>
<td>174425235</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>0</td>
<td>0.242</td>
<td>26560625</td>
<td>109754648</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>6</td>
<td>0.36</td>
<td>51191219</td>
<td>142197830</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.929</td>
<td>168771687</td>
<td>181670276</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.626</td>
<td>43705622</td>
<td>69817287</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>6</td>
<td>4.256</td>
<td>973544606</td>
<td>228746382</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>2.315</td>
<td>169047118</td>
<td>73022513</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>4</td>
<td>0.816</td>
<td>115350803</td>
<td>141361278</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>28</td>
<td>4.137</td>
<td>822747204</td>
<td>198875321</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>16</td>
<td>6.387</td>
<td>1021389690</td>
<td>159916970</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>10</td>
<td>15.945</td>
<td>3470416861</td>
<td>217649223</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>a3</td>
<td>6</td>
<td>19.308</td>
<td>2093326335</td>
<td>108417564</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>0</td>
<td>7.95</td>
<td>666596389</td>
<td>83848602</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>67.989</td>
<td>12227417145</td>
<td>179844050</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>71.954</td>
<td>13290990536</td>
<td>184715103</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>b7</td>
<td>0</td>
<td>276.5</td>
<td>41506305139</td>
<td>150113219</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>2</td>
<td>28.172</td>
<td>3409497345</td>
<td>121024327</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>88.863</td>
<td>13317806725</td>
<td>149868974</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>4</td>
<td>31.941</td>
<td>4861384409</td>
<td>152198879</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>g8</td>
<td>64</td>
<td>1.624</td>
<td>2975</td>
<td>1831</td>
</tr>
<tr>
<td>全体</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>630.501</td>
<td>98268669952</td>
<td>155858072</td>
</tr>
</table>







## Edax4.4との対戦

現状世界最強とも言われるオセロAI、<a href="https://github.com/abulmo/edax-reversi" target="_blank" el=”noopener noreferrer”>Edax 4.4</a>との対戦結果です。

初手からの対戦では同じ進行ばかりになって評価関数の強さは計測できないので、初期局面から8手進めた互角に近いと言われる状態から打たせて勝敗を数えました。このとき、同じ進行に対して両者が必ず先手と後手の双方を1回ずつ持つようにしました。こうすることで、両者の強さが全く同じであれば勝率は50%となるはずです。

テストには<a href="https://berg.earthlingz.de/xot/index.php" target="_blank" el=”noopener noreferrer”>XOT</a>に収録されている局面を使用しました。

bookは双方未使用です。

Egaroucid勝率が0.5を上回っていればEgaroucidがEdaxに勝ち越しています。

### Egaroucidが黒番

<table>
<tr>
<th>レベル</th>
<th>Egaroucid勝ち</th>
<th>引分</th>
<th>Edax勝ち</th>
<th>Egaroucid勝率</th>
</tr>
<tr>
<td>1</td>
<td>61</td>
<td>2</td>
<td>67</td>
<td>0.48</td>
</tr>
<tr>
<td>5</td>
<td>68</td>
<td>6</td>
<td>56</td>
<td>0.55</td>
</tr>
<tr>
<td>11</td>
<td>69</td>
<td>18</td>
<td>43</td>
<td>0.62</td>
</tr>
</table>




### Egaroucidが白番

<table>
<tr>
<th>レベル</th>
<th>Egaroucid勝ち</th>
<th>引分</th>
<th>Edax勝ち</th>
<th>Egaroucid勝率</th>
</tr>
<tr>
<td>1</td>
<td>76</td>
<td>3</td>
<td>51</td>
<td>0.6</td>
</tr>
<tr>
<td>5</td>
<td>67</td>
<td>11</td>
<td>52</td>
<td>0.56</td>
</tr>
<tr>
<td>11</td>
<td>61</td>
<td>15</td>
<td>54</td>
<td>0.53</td>
</tr>
</table>
