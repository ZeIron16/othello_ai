# Egaroucid 7.0.0 ベンチマーク

## The FFO endgame test suite

<a href="http://radagast.se/othello/ffotest.html" target="_blank" el=”noopener noreferrer”>The FFO endgame test suite</a>はオセロAIの終盤探索力の指標として広く使われるベンチマークです。各テストケースを完全読みし、最善手を計算します。探索時間と訪問ノード数を指標に性能を評価します。NPSはNodes Per Secondの略で、1秒あたりの訪問ノード数を表します。

### Egaroucid for Console 7.0.0 Windows x64 SIMD


#### Core i9 13900K @ 32並列

<div class="table_wrapper">
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
<tr>
<td>#40</td>
<td>20</td>
<td>a2</td>
<td>+38</td>
<td>0.016</td>
<td>13095826</td>
<td>818489125</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>+0</td>
<td>0.054</td>
<td>31733978</td>
<td>587666259</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>+6</td>
<td>0.066</td>
<td>49405340</td>
<td>748565757</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.149</td>
<td>118010790</td>
<td>792018724</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.041</td>
<td>18079308</td>
<td>440958731</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>+6</td>
<td>0.291</td>
<td>322619250</td>
<td>1108657216</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>0.134</td>
<td>90700458</td>
<td>676869089</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>+4</td>
<td>0.1</td>
<td>88624182</td>
<td>886241820</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>+28</td>
<td>0.218</td>
<td>157234062</td>
<td>721257165</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>+16</td>
<td>0.464</td>
<td>399676639</td>
<td>861372066</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>+10</td>
<td>0.947</td>
<td>755470579</td>
<td>797751403</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>e2</td>
<td>+6</td>
<td>0.432</td>
<td>386349187</td>
<td>894326821</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>+0</td>
<td>0.483</td>
<td>403634351</td>
<td>835681886</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>2.562</td>
<td>2519470056</td>
<td>983399709</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>3.984</td>
<td>3983373384</td>
<td>999842716</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>g6</td>
<td>+0</td>
<td>12.398</td>
<td>11082195535</td>
<td>893869618</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>+2</td>
<td>1.404</td>
<td>1017876893</td>
<td>724983542</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>3.098</td>
<td>2871440500</td>
<td>926869109</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>+4</td>
<td>1.827</td>
<td>1556662686</td>
<td>852032121</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>h4</td>
<td>+64</td>
<td>0.054</td>
<td>17365258</td>
<td>321578851</td>
</tr>
<tr>
<td>全体</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>28.722</td>
<td>25883018262</td>
<td>901156544</td>
</tr>
</table>
</div>



### Egaroucid for Console 7.0.0 Windows x64 Generic

SIMDによる高速化をしていないバージョンです。

#### Core i9 13900K @ 32並列

<div class="table_wrapper">
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
<tr>
<td>#40</td>
<td>20</td>
<td>a2</td>
<td>+38</td>
<td>0.029</td>
<td>13745836</td>
<td>473994344</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>+0</td>
<td>0.089</td>
<td>32685564</td>
<td>367253528</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>+6</td>
<td>0.117</td>
<td>51731192</td>
<td>442146940</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.242</td>
<td>114425926</td>
<td>472834404</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.069</td>
<td>18898575</td>
<td>273892391</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>+6</td>
<td>0.506</td>
<td>317687190</td>
<td>627840296</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>0.203</td>
<td>84792202</td>
<td>417695576</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>+4</td>
<td>0.089</td>
<td>24700626</td>
<td>277535123</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>+28</td>
<td>0.407</td>
<td>195897969</td>
<td>481321791</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>+16</td>
<td>0.677</td>
<td>327109235</td>
<td>483174645</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>+10</td>
<td>1.733</td>
<td>788308775</td>
<td>454881001</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>e2</td>
<td>+6</td>
<td>1.088</td>
<td>634944238</td>
<td>583588454</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>+0</td>
<td>0.826</td>
<td>407859964</td>
<td>493777196</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>4.27</td>
<td>2456352890</td>
<td>575258288</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>6.384</td>
<td>3801732457</td>
<td>595509470</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>g6</td>
<td>+0</td>
<td>20.773</td>
<td>11459161935</td>
<td>551637314</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>+2</td>
<td>2.391</td>
<td>1041524297</td>
<td>435601964</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>4.686</td>
<td>2579060408</td>
<td>550375673</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>+4</td>
<td>3.607</td>
<td>1855300695</td>
<td>514361157</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>h4</td>
<td>+64</td>
<td>0.089</td>
<td>17164869</td>
<td>192863696</td>
</tr>
<tr>
<td>全体</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>48.275</td>
<td>26223084843</td>
<td>543202172</td>
</tr>
</table>
</div>



## Edax 4.4との対戦

現状世界最強とも言われるオセロAI、<a href="https://github.com/abulmo/edax-reversi" target="_blank" el=”noopener noreferrer”>Edax 4.4</a>との対戦結果です。

初手からの対戦では同じ進行ばかりになって評価関数の強さは計測できないので、初期局面から8手進めた互角に近いと言われる状態から打たせて勝敗を数えました。このとき、同じ進行に対して両者が必ず先手と後手の双方を1回ずつ持つようにしました。こうすることで、両者の強さが全く同じであれば勝率は50%となるはずです。

テストには<a href="https://berg.earthlingz.de/xot/index.php" target="_blank" el=”noopener noreferrer”>XOT</a>に収録されている局面を使用しました。

bookは双方未使用です。

Egaroucid勝率が0.5を上回っていればEgaroucidがEdaxに勝ち越しています。また、カッコ内の数字はEgaroucidが黒番/白番のときのそれぞれの値です。全ての条件でEgaroucidが勝ち越しています。

バージョン6.3.0までは引き分けを省いて(勝ち)/(勝ち+負け)で勝率を計算していましたが、一般的ではなかったので、バージョン6.4.0からは引き分けを0.5勝として(勝ち+0.5*引き分け)/(勝ち+引き分け+負け)で計算しました。

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
<td>1217(黒: 589 白: 628)</td>
<td>47(黒: 17 白: 30)</td>
<td>736(黒: 394 白: 342)</td>
<td>0.62</td>
</tr>
<tr>
<td>5</td>
<td>1189(黒: 599 白: 590)</td>
<td>108(黒: 54 白: 54)</td>
<td>703(黒: 347 白: 356)</td>
<td>0.622</td>
</tr>
<tr>
<td>10</td>
<td>904(黒: 500 白: 404)</td>
<td>236(黒: 120 白: 116)</td>
<td>860(黒: 380 白: 480)</td>
<td>0.511</td>
</tr>
<tr>
<td>15</td>
<td>232(黒: 128 白: 104)</td>
<td>94(黒: 43 白: 51)</td>
<td>174(黒: 79 白: 95)</td>
<td>0.558</td>
</tr>
<tr>
<td>21</td>
<td>81(黒: 49 白: 32)</td>
<td>60(黒: 30 白: 30)</td>
<td>59(黒: 21 白: 38)</td>
<td>0.555</td>
</tr>
</table>



