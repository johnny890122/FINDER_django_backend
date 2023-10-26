## Backend
```
python3 -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip3 install -r requirements.txt
otree devserver
```

## Frontend

frontend 資料夾是可以獨立運作的 React 專案。

```
cd frontend 
npm install (first time)
npm start (平常 debug 用)
npm run build (for otree 前端)
```

### build
- npm run build 後，會將 build 後的檔案放到 `build_for_test/`
- 這個資料夾下面的檔案，名字可以對應到 `page.py` 裡面的 class。

## 前端 -> 後端
我目前是把 otree 的前端直接複製過來，就可以順利把前端輸入的資料，送到 otree 後臺。
請見 frontend/src/App.js 中的 const App。

### 可優化之處
目前還不確定到底是哪些 component 起作用，我們可以再試試看，找到最簡化的 component 結構。

## 後端到前端
這個部分是比較多問題的地方，我看 otree 和 react 的前後端溝通，其實有非常多種方式。
我目前嘗試了在前端直接用 api 的方式，具體如下：

App.js 的 useEffect 中，有一個 axios.get("http://localhost:8000/api/")，表示
前端會呼叫 http://localhost:8000/api/ 這個 api。

我們需要在 django 後臺定義這個 api，在 urls.py 這個檔案中，有一個 path('api/', Index.vars_for_react),
的函數，p.s. from build_for_test.pages import Index。

也就是說，打這個網址後，我們要呼叫 Index.vars_for_react。
    def vars_for_react(self):
        template = {
            "test": "Hello World!"
        }

## 需要優化之處：
1. 目前還沒辦法呼叫 subpath，也就是像 http://localhost:8000/api/123 這類的 api。
2. 目前還沒辦法在 api 加入 argument，例如 user id 這種可以辨別資訊的 arguemnt。
3. 我猜在 session 建立時，必須要有一個機制，將 ex user_id 這種資訊，送到 react，讓 react 可以保存。
    之後前端可以使用這個識別碼，向後端 query 資料。
4. 我覺得另一種方式是，利用像 GraphQL 那樣的技術，讓前端可以向 otree 的 db 要資料。但這種方式可能僅限於，
    會被紀錄進去 db 的那些 filed。因為在 otree 中，有很多像是現在第幾回合這種資訊，並不會被紀錄進去 db，
    只是單純 for 前端使用而已。
5. 其他．．．