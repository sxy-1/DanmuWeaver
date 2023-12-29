
  <h1 align="center">
  弹幕编织者
</h1>

<p align="center">
  基于 phash/DTW 计算弹幕偏移时间
</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>
</p>



### 介绍

当前大环境下，观看动漫中被“和谐”掉的画面越来越多，极其影响观看体验，不少人放弃正版环境，选择前往盗版网站观看完整视频，可是又失去了弹幕/评论的氛围感。本实验尝试使用机器学习算法，让弹幕迁移到完整视频，获得更好的观看体验。

![image-20231229222406456](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202312292224590.png)





### 效果展示

（版权问题不方便放图，以后再补）

但是效果还是很好的，在第三方下载的视频，可以有准确的弹幕体验。





### 流程

1.下载原视频（以下称为L视频），和谐视频（以下称为S视频），以及和谐视频对应的弹幕（S弹幕）2.通过感知哈希函数对每一帧进行计算
3.进行dtw运算，得出最优路径
4.根据最优路径的映射关系，生成新弹幕
5.加载至完整视频



### 参考

[DTW（动态时间规整）算法原理与应用_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV12r4y1A7mT/?spm_id_from=333.788&vd_source=df034c933ea08326f3a58a38fa1c7fce)
 [鸣梦 - 博客园 (cnblogs.com)](https://www.cnblogs.com/HoEn/)



### 其他

本项目由于作者时间不允许，只使用tkinter，并发现pyinstaller后无法运行，将在今后半年转为pyqt，并提供友好客户端。





### 许可证

使用 GPLv3 许可证.

Copyright © 2023 by dullspear

