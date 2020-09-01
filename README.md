# Factsheet - Stock factsheet command-line tool

Quick and easy command-line tool to display stock factsheet

## Usage

```
$ export ALPHAVANTAGE_APIKEY="YOUR_API_KEY"
$ factsheet
Usage:
factsheet <TICKER SYMBOL>
Example: factsheet TSLA
```

## Output

```
$ factsheet IBM
IBM | International Business Machines Corporation | Technology
Common Stock

123.31 -1.76 (-1.41%)
2020-08-31 | USD | NYSE

Previous Close           125.07 | Market Cap               109.8B
Open                   125.2500 | Beta                       1.21
Day's Range       123.03-125.25 | PE Ratio                  14.13
52 Week Range      90.56-158.75 | EPS                        8.81
Volume                    4.83M | Dividend                   6.52

                         1 Week         1 Month        3 Months          1 Year         3 Years         5 Years
Performance              -1.07%           1.61%          -3.20%          -4.49%          -1.75%           3.93%
High                     125.30          130.47          135.88          158.75          171.13          182.79
Low                      123.03          122.15          115.20           90.56           90.56           90.56

Chart: 1 Year

  160 +-------------------------------------------------------------------------------------------------------------------------------------------+
      |                                                                                                                                           |
      |                                                                                       International Business Machines Corporation ******* |
      |                                                                                                                                           |
      |                                                                                                                                           |
      |                                                                                                                                           |
      |                                                               ****                                                                        |
  150 |                                                               * **                                                                        |
      |                                                               *  ***                                                                      |
      |                                                              *   * *                                                                      |
      |                                                              *      *                                                                     |
      |                                                              *      *                                                                     |
      |                                                              *      *                                                                     |
  140 |                                                              *       *                                                                    |
      |            *     **                                      *  *        *                                                                    |
      |            **   * *                                      *  *        *                                                                    |
      |           *  **** ** ***                                 ** *        *                                                                    |
      |          *          ** *                                ** **        *                                   *                                |
      |          *          ** *      **                       *   **        *                                   *                                |
      |          *          *  *      * *    *     *  *** * ***     *        * *                                **                                |
  130 |          *             *  ****   ******   **** ******                * *                                **                                |
      |         *              **** *      *   ***       *                    ***                              * *                                |
      |                          *              *                             ***                              * *              *     **          |
      |                                                                        **                  *           * *             ****  * *** ***    |
      |                                                                         *                 **        ***  * *          * * * **   ** * *   |
      |                                                                         * *              ***  *     *     ***        **    **             |
  120 |                                                                         * *           *  * * *** ** *     ***        *                    |
      |                                                                          **         * *  * ***** ** *     *  *  ***  *                    |
      |                                                                          **         ******     ** **      *   * ** ***                    |
      |                                                                          **         * ***       *         *   **   **                     |
      |                                                                          **         * * *       *             *    *                      |
      |                                                                           *        *  *                                                   |
      |                                                                           *        *                                                      |
  110 |                                                                           *    **  *                                                      |
      |                                                                           *    *** *                                                      |
      |                                                                           *    * **                                                       |
      |                                                                           **   * **                                                       |
      |                                                                           ***  * **                                                       |
      |                                                                           *** *  *                                                        |
  100 |                                                                           * * *                                                           |
      |                                                                             ***                                                           |
      |                                                                             ***                                                           |
      |                                                                             ***                                                           |
      |                                                                              **                                                           |
      |                                                                              **                                                           |
      |                                                                                                                                           |
   90 +-------------------------------------------------------------------------------------------------------------------------------------------+
  1.565e+09            1.57e+09           1.575e+09            1.58e+09           1.585e+09            1.59e+09           1.595e+09            1.6e+09

```
