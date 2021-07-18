# rush-purchase

本抢购脚本用的是chrome浏览器，需要下载chromedriver，
在浏览器里输入chrome://version/查看chrome版本，
然后在http://chromedriver.storage.googleapis.com/index.html
下载对应chrome版本、对应你的系统的chromedriver，最后将其放入环境变量中。
windows下载下来的是chromedriver.exe，然后将下载好的chromedriver.exe文件放置到chrome浏览器所在目录，
同时将该目录配置到Windows系统环境变量中。
mac有homebrew的话，直接执行brew install chromedriver即可完成下载与配置。
这样脚本就能执行webdriver.Chrome()，如果因某些原因无法配置环境变量，或配置失败，
则需要把脚本中的webdriver.Chrome()都改成webdriver.Chrome(r"你下载下来的chromedriver的全路径")，来完成chromedriver的加载。