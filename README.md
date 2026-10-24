# tv-trailer

The trailer player for my Free My TV build on a Samsung TV. Installed TV apps run from a local file, so YouTube gets no
address from them and refuses to play embedded trailers (error 153). Free My TV embeds this page instead
(`trailer_page` in its `config.properties`), and YouTube sees this page's address.

`index.html?v=<YouTube id>&hl=<language>` plays the video and tells the parent window when it ends or can't play.
Source: `docs/trailer/index.html` in my local Free My TV checkout (github.com/simbasjungles/free-my-tv).

## Netflix Top 10

`top10.json` is Netflix's official weekly Top 10 for Germany, cut down from Netflix's full file
(netflix.com/tudum/top10) by `top10.py`. The Pages workflow builds it every Tuesday and Wednesday and on every push.
