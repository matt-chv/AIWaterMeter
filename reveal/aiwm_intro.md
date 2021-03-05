# AIWM - intro

![](../static/img/maze_with_help_grey.png)

> Are you lost, not sure where to start let alone where to go?
Why ? Wieso ? Pourquoi ? 为什么?


Notes: Make it clear this is for those who think they need sensor fusion but not sure why, nor what it is let alone how to make it work
We will try in the next 20mn to answer those questions.
* Why would you need sensor fusion
* What is sensor fusion
* How can you get your first PoC and secure a path to production

---

## Why are we meeting today?

* To discuss AI / ML generally
* Share update about the AIWM
* Discuss next steps

----

<!-- .slide: data-background-iframe="https://matt-chv.github.io/AIWaterMeter/reveal/ai_news.html#/" data-background-interactive-->

<div style="position: absolute; width: 30%; right: -400px; box-shadow: 0 1px 4px rgba(0,0,0,0.5), 0 5px 25px rgba(0,0,0,0.2); background-color: rgba(0, 0, 0, 0.9); color: #fff; padding: 20px; font-size: 20px; text-align: left;">
    <h2>mmWave and vision fusion in ROS </h2>
  <ul> 
    <li> Why re-invent the wheel? </li></span>
    <span class="fragment"><li> Reveal is cool - allows slideset nesting </li></span>
    <span class="fragment"><li> MVC: keep data and rendering separate </li></span>
    <span class="fragment"><li> ...  </li></span>
  </ul>
</div>

---

## AIWM update

0. The project overview <!-- .element: class="fragment" data-fragment-index="1" -->
1. Project update <!-- .element: class="fragment" data-fragment-index="2" -->
2. Project next step <!-- .element: class="fragment" data-fragment-index="3" -->

----

### AIWM Overview

* 3D printed casing
* ESP32+camera module
* MQTT messages
* CNN for image processing

----

### Project udpate - CNN processing

* training on gauges - OKish
* training on numbers - TBD
* github repo - ok
* wiki - started

----

### Project next steps

* Find why training does not work on Win10 (at least for Matt)
* non-regression testing for incremental changes on code
* find more training data (see issue list)
* more ?

