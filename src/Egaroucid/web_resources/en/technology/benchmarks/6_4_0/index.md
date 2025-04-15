# Egaroucid 6.4.0 Benchmarks

## The FFO endgame test suite

<a href="http://radagast.se/othello/ffotest.html" target="_blank" el=”noopener noreferrer”>The FFO endgame test suite</a> is a common benchmark for endgame searching. Computer completely solves each testcase, and find the best move. This benchmark evaluates the exact time for searching and the speed (NPS: Nodes Per Second).

### Egaroucid for Console 6.4.0 Windows x64 SIMD


#### Core i9 13900K @ 32 threads

<div class="table_wrapper"><table>
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
<td>20</td>
<td>a2</td>
<td>+38</td>
<td>0.037</td>
<td>18551129</td>
<td>501381864</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>+0</td>
<td>0.063</td>
<td>26869773</td>
<td>426504333</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>+6</td>
<td>0.123</td>
<td>71405077</td>
<td>580529081</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>g3</td>
<td>-12</td>
<td>0.183</td>
<td>102405636</td>
<td>559593639</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>b8</td>
<td>-14</td>
<td>0.071</td>
<td>21069844</td>
<td>296758366</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>+6</td>
<td>0.466</td>
<td>416937288</td>
<td>894715210</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>0.177</td>
<td>92389718</td>
<td>521975807</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>+4</td>
<td>0.091</td>
<td>23819448</td>
<td>261752175</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>+28</td>
<td>0.353</td>
<td>168442255</td>
<td>477173526</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>+16</td>
<td>0.46</td>
<td>319391867</td>
<td>694330145</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>+10</td>
<td>1.629</td>
<td>1145908606</td>
<td>703442974</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>e2</td>
<td>+6</td>
<td>0.855</td>
<td>587578234</td>
<td>687226004</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>+0</td>
<td>0.688</td>
<td>440750924</td>
<td>640626343</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>3.701</td>
<td>2689891689</td>
<td>726801320</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>5.462</td>
<td>5001985645</td>
<td>915779136</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>g6</td>
<td>+0</td>
<td>14.02</td>
<td>10545655917</td>
<td>752186584</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>+2</td>
<td>1.855</td>
<td>918717949</td>
<td>495265740</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>2.95</td>
<td>1918737622</td>
<td>650419532</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>+4</td>
<td>2.433</td>
<td>1364592150</td>
<td>560868125</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>e8</td>
<td>+64</td>
<td>0.469</td>
<td>6199035</td>
<td>13217558</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>36.086</td>
<td>25881299806</td>
<td>717211656</td>
</tr>
    </table></div>



### Egaroucid for Console 6.4.0 Windows x64 Generic

Without speedup by SIMD

#### Core i9 13900K @ 32 threads

<div class="table_wrapper"><table>
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
<td>20</td>
<td>a2</td>
<td>+38</td>
<td>0.04</td>
<td>15910301</td>
<td>397757525</td>
</tr>
<tr>
<td>#41</td>
<td>22</td>
<td>h4</td>
<td>+0</td>
<td>0.086</td>
<td>24980177</td>
<td>290467174</td>
</tr>
<tr>
<td>#42</td>
<td>22</td>
<td>g2</td>
<td>+6</td>
<td>0.187</td>
<td>78603581</td>
<td>420340005</td>
</tr>
<tr>
<td>#43</td>
<td>23</td>
<td>c7</td>
<td>-12</td>
<td>0.167</td>
<td>66554688</td>
<td>398531065</td>
</tr>
<tr>
<td>#44</td>
<td>23</td>
<td>d2</td>
<td>-14</td>
<td>0.075</td>
<td>13925836</td>
<td>185677813</td>
</tr>
<tr>
<td>#45</td>
<td>24</td>
<td>b2</td>
<td>+6</td>
<td>0.73</td>
<td>404624370</td>
<td>554279958</td>
</tr>
<tr>
<td>#46</td>
<td>24</td>
<td>b3</td>
<td>-8</td>
<td>0.238</td>
<td>85301685</td>
<td>358410441</td>
</tr>
<tr>
<td>#47</td>
<td>25</td>
<td>g2</td>
<td>+4</td>
<td>0.091</td>
<td>22426387</td>
<td>246443813</td>
</tr>
<tr>
<td>#48</td>
<td>25</td>
<td>f6</td>
<td>+28</td>
<td>0.508</td>
<td>174331347</td>
<td>343171942</td>
</tr>
<tr>
<td>#49</td>
<td>26</td>
<td>e1</td>
<td>+16</td>
<td>0.756</td>
<td>389448889</td>
<td>515144033</td>
</tr>
<tr>
<td>#50</td>
<td>26</td>
<td>d8</td>
<td>+10</td>
<td>2.549</td>
<td>1151727651</td>
<td>451835092</td>
</tr>
<tr>
<td>#51</td>
<td>27</td>
<td>e2</td>
<td>+6</td>
<td>1.231</td>
<td>560750484</td>
<td>455524357</td>
</tr>
<tr>
<td>#52</td>
<td>27</td>
<td>a3</td>
<td>+0</td>
<td>1.165</td>
<td>516146220</td>
<td>443043965</td>
</tr>
<tr>
<td>#53</td>
<td>28</td>
<td>d8</td>
<td>-2</td>
<td>6.587</td>
<td>3314489603</td>
<td>503186519</td>
</tr>
<tr>
<td>#54</td>
<td>28</td>
<td>c7</td>
<td>-2</td>
<td>8.898</td>
<td>5070789929</td>
<td>569879740</td>
</tr>
<tr>
<td>#55</td>
<td>29</td>
<td>g6</td>
<td>+0</td>
<td>22.012</td>
<td>10713139055</td>
<td>486695395</td>
</tr>
<tr>
<td>#56</td>
<td>29</td>
<td>h5</td>
<td>+2</td>
<td>2.81</td>
<td>1037039643</td>
<td>369053253</td>
</tr>
<tr>
<td>#57</td>
<td>30</td>
<td>a6</td>
<td>-10</td>
<td>5.86</td>
<td>2882233211</td>
<td>491848670</td>
</tr>
<tr>
<td>#58</td>
<td>30</td>
<td>g1</td>
<td>+4</td>
<td>3.672</td>
<td>1454112944</td>
<td>396000257</td>
</tr>
<tr>
<td>#59</td>
<td>34</td>
<td>e8</td>
<td>+64</td>
<td>0.522</td>
<td>7485471</td>
<td>14339982</td>
</tr>
<tr>
<td>All</td>
<td>-</td>
<td>-</td>
<td>-</td>
<td>58.184</td>
<td>27984021472</td>
<td>480957333</td>
</tr>
    </table></div>






## Play against Edax 4.4

<a href="https://github.com/abulmo/edax-reversi" target="_blank" el=”noopener noreferrer”>Edax 4.4</a> is one of the best Othello AI in the world.

If I set the game from the very beginning, same line appears a lot. To avoid this, I set the game from many different near-draw lines.

I used <a href="https://berg.earthlingz.de/xot/index.php" target="_blank" el=”noopener noreferrer”>XOT</a> for its testcases.

No opening books used.

If Egaroucid Win Ratio is over 0.5, then Egaroucid wins more than Edax do. "Black" and "White" means Egaroucid played black/white. In all conditions, Egaroucid is stronger than Edax.

<div class="table_wrapper"><table>
<tr>
<th>Level</th>
<th>Egaroucid win</th>
<th>Draw</th>
<th>Edax Win</th>
<th>Egaroucid Win Ratio</th>
</tr>
<tr>
<td>1</td>
<td>1246(Black: 602 White: 644)</td>
<td>59(Black: 29 White: 30)</td>
<td>695(Black: 369 White: 326)</td>
<td>0.638</td>
</tr>
<tr>
<td>5</td>
<td>1152(Black: 586 White: 566)</td>
<td>101(Black: 50 White: 51)</td>
<td>747(Black: 364 White: 383)</td>
<td>0.601</td>
</tr>
<tr>
<td>10</td>
<td>1062(Black: 623 White: 439)</td>
<td>223(Black: 97 White: 126)</td>
<td>715(Black: 280 White: 435)</td>
<td>0.587</td>
</tr>
<tr>
<td>15</td>
<td>480(Black: 234 White: 246)</td>
<td>159(Black: 74 White: 85)</td>
<td>361(Black: 192 White: 169)</td>
<td>0.559</td>
</tr>
<tr>
<td>21</td>
<td>86(Black: 56 White: 30)</td>
<td>52(Black: 25 White: 27)</td>
<td>62(Black: 19 White: 43)</td>
<td>0.56</td>
</tr>
    </table></div>


