# Egaroucid 6.1.0 Benchmarks

## The FFO endgame test suite

<a href="http://radagast.se/othello/ffotest.html" target="_blank" el=”noopener noreferrer”>The FFO endgame test suite</a> is a common benchmark for endgame searching. Computer completely solves each testcase, and find the best move. This benchmark evaluates the exact time for searching and the speed (NPS: Nodes Per Second).

I used Core i9-11900K for testing.

### Egaroucid for Console 6.1.0 Windows x64 SIMD

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
<tr>
<td>#40</td>
<td>20@100%</td>
<td>a2</td>
<td>+38</td>
<td>0.13</td>
<td>34046159</td>
<td>261893530</td>
</tr>
<tr>
<td>#41</td>
<td>22@100%</td>
<td>h4</td>
<td>+0</td>
<td>0.233</td>
<td>38361379</td>
<td>164641111</td>
</tr>
<tr>
<td>#42</td>
<td>22@100%</td>
<td>g2</td>
<td>+6</td>
<td>0.324</td>
<td>69392367</td>
<td>214173972</td>
</tr>
<tr>
<td>#43</td>
<td>23@100%</td>
<td>c7</td>
<td>-12</td>
<td>0.284</td>
<td>57083578</td>
<td>200998514</td>
</tr>
<tr>
<td>#44</td>
<td>23@100%</td>
<td>b8</td>
<td>-14</td>
<td>0.198</td>
<td>21367458</td>
<td>107916454</td>
</tr>
<tr>
<td>#45</td>
<td>24@100%</td>
<td>b2</td>
<td>+6</td>
<td>1.813</td>
<td>612227091</td>
<td>337687308</td>
</tr>
<tr>
<td>#46</td>
<td>24@100%</td>
<td>b3</td>
<td>-8</td>
<td>0.516</td>
<td>104353321</td>
<td>202235118</td>
</tr>
<tr>
<td>#47</td>
<td>25@100%</td>
<td>g2</td>
<td>+4</td>
<td>0.247</td>
<td>30154429</td>
<td>122082708</td>
</tr>
<tr>
<td>#48</td>
<td>25@100%</td>
<td>f6</td>
<td>+28</td>
<td>0.896</td>
<td>178317496</td>
<td>199015062</td>
</tr>
<tr>
<td>#49</td>
<td>26@100%</td>
<td>e1</td>
<td>+16</td>
<td>1.693</td>
<td>461193080</td>
<td>272411742</td>
</tr>
<tr>
<td>#50</td>
<td>26@100%</td>
<td>d8</td>
<td>+10</td>
<td>6.572</td>
<td>2078435981</td>
<td>316256235</td>
</tr>
<tr>
<td>#51</td>
<td>27@100%</td>
<td>e2</td>
<td>+6</td>
<td>1.819</td>
<td>402752110</td>
<td>221414024</td>
</tr>
<tr>
<td>#52</td>
<td>27@100%</td>
<td>a3</td>
<td>+0</td>
<td>2.105</td>
<td>460196375</td>
<td>218620605</td>
</tr>
<tr>
<td>#53</td>
<td>28@100%</td>
<td>d8</td>
<td>-2</td>
<td>16.745</td>
<td>5428631290</td>
<td>324194164</td>
</tr>
<tr>
<td>#54</td>
<td>28@100%</td>
<td>c7</td>
<td>-2</td>
<td>20.264</td>
<td>6858449925</td>
<td>338454891</td>
</tr>
<tr>
<td>#55</td>
<td>29@100%</td>
<td>g6</td>
<td>+0</td>
<td>56.476</td>
<td>14231640162</td>
<td>251994478</td>
</tr>
<tr>
<td>#56</td>
<td>29@100%</td>
<td>h5</td>
<td>+2</td>
<td>7.647</td>
<td>1421292685</td>
<td>185862780</td>
</tr>
<tr>
<td>#57</td>
<td>30@100%</td>
<td>a6</td>
<td>-10</td>
<td>14.908</td>
<td>4174615559</td>
<td>280025191</td>
</tr>
<tr>
<td>#58</td>
<td>30@100%</td>
<td>g1</td>
<td>+4</td>
<td>8.619</td>
<td>1762391815</td>
<td>204477528</td>
</tr>
<tr>
<td>#59</td>
<td>34@100%</td>
<td>e8</td>
<td>+64</td>
<td>0.129</td>
<td>627770</td>
<td>4866434</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>141.618</td>
<td>38425530030</td>
<td>271332246</td>
</tr>
</table>







## Play against Edax4.4

<a href="https://github.com/abulmo/edax-reversi" target="_blank" el=”noopener noreferrer”>Edax 4.4</a> is one of the best Othello AI in the world.

If I set the game from the very beginning, same line appears a lot. To avoid this, I set the game from many different near-draw lines.

I used <a href="https://berg.earthlingz.de/xot/index.php" target="_blank" el=”noopener noreferrer”>XOT</a> for its testcases.

No opening books used.

If Egaroucid Win Ratio is over 0.5, then Egaroucid wins more than Edax do. "Black" and "White" means Egaroucid played black/white. In all conditions, Egaroucid is stronger than Edax.

<table>
<tr>
<th>Level</th>
<th>Egaroucid win</th>
<th>Draw</th>
<th>Edax Win</th>
<th>Egaroucid Win Ratio</th>
</tr>
<tr>
<td>1</td>
<td>1281(Black: 643 White: 638)</td>
<td>40(Black: 21 White: 19)</td>
<td>679(Black: 336 White: 343)</td>
<td>0.654</td>
</tr>
<tr>
<td>5</td>
<td>1189(Black: 609 White: 580)</td>
<td>95(Black: 51 White: 44)</td>
<td>716(Black: 340 White: 376)</td>
<td>0.624</td>
</tr>
<tr>
<td>10</td>
<td>1045(Black: 587 White: 458)</td>
<td>247(Black: 112 White: 135)</td>
<td>708(Black: 301 White: 407)</td>
<td>0.596</td>
</tr>
<tr>
<td>15</td>
<td>107(Black: 63 White: 44)</td>
<td>35(Black: 11 White: 24)</td>
<td>58(Black: 26 White: 32)</td>
<td>0.648</td>
</tr>
</table>
