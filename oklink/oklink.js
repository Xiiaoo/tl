
// token=crypto.randomUUID()


i = ""
for (a = crypto.subtle.digest("SHA-256",(new TextEncoder).encode("7df19d92-eaed-48a7-b0fb-cd2cd49d6363")),
    c = [247,9,156,29,139,248,216,138,94,214,186,131,159,194,102,226,70,100,237,19,136,45,185,236,235,125,252,50,155,19,155,139],
    u = c.map((function(e) {
        return e.toString(16).padStart(2, "0")
    }
    )).join(""),
    s = Math.floor(Date.now() / 1e3),
    l = Math.floor(s / 600 % 32),
    f = Math.floor(s / 3600 % 32),
    d = 0; d < 32; d++)
        p = u[(l + (f + d) * d) % 32],
        i += p;

console.log(i, )
// crypto.subtle.importKey 方法在 Web Cryptography API 中用于将密钥材料（如从文件、数据库或网络传输中获取的密钥数据）导入为 CryptoKey 对象
CKey=crypto.subtle.importKey("raw", (new TextEncoder).encode("f469ee964fb2e87a373b33b373a78e2b"), {
    name: "HMAC",
    hash: "SHA-256"
}, !1, ["sign"])


// console.log(CKey, )

// crypto.subtle.digest("SHA-256", (new TextEncoder).encode("d0d97aa5-8378-448b-b018-eb5f08a73d2b"));
// crypto.subtle.importKey("raw", (new TextEncoder).encode(i), {
//     name: "HMAC",
//     hash: "SHA-256"
// }, !1, ["sign"]);
// 







console.log(crypto.subtle.digest("SHA-256",(new TextEncoder).encode("397197b8-c1a2-459d-b369-b66f1d68b39f")))
// console.log((new TextEncoder).encode("/api/explorer/v1/btc/transactionsNoRestrictoffset=100&limit=20&t=1724397135566"))
aa=btoa(String.fromCharCode.apply(String, [114,62,98,70,26,249,252,228,196,19,59,220,18,40,105,10,133,138,176,158,19,144,102,188,209,109,95,151,148,140,152,107]))
console.log(aa, )









// aaa={
//     url: "/api/explorer/v1/btc/transactionsNoRestrict?offset=80&limit=20&t=1724404331368",
//     fetchConfig: {
//         method: "get"
//     },
//     token: "2759cc79-dfee-44bd-9bd6-681830ef04a8"
// }

bbb={
    token: "2759cc79-dfee-44bd-9bd6-681830ef04a8",
    timestampForTest: undefined
}


// 1
console.log('111111',crypto.subtle.digest("SHA-256", (new TextEncoder).encode("1fec7a89-d5f6-411b-8f24-c21caa8719e7")))


// for (a = e.sent,
//     c = Array.from(new Uint8Array(a)),
//     u = c.map((function(e) {
//         return e.toString(16).padStart(2, "0")
//     }
//     )).join(""),
//     s = o || Math.floor(Date.now() / 1e3),
//     l = Math.floor(s / 600 % 32),
//     f = Math.floor(s / 3600 % 32),
//     d = 0; d < 32; d++)
//         p = u[(l + (f + d) * d) % 32],
//         i += p;

// // encode i
// crypto.subtle.importKey("raw", (new TextEncoder).encode("3133134a272ac58f77ff77f85ca272a4"), {
//     name: "HMAC",
//     hash: "SHA-256"
// }, !1, ["sign"]);


// "/api/explorer/v1/btc/transactionsNoRestrictoffset=200&limit=20&curType=large&sort=realTransferValue%2Cdesc&t=1724412021256"
// crypto.subtle.sign("HMAC", c, (new TextEncoder).encode(u))

// d = btoa(String.fromCharCode.apply(String, ye(new Uint8Array(f))))\


async function generateHMAC() {  
    try {  
        // 导入密钥  
        const key = await crypto.subtle.importKey(  
            "raw",  
            (new TextEncoder()).encode("f469ee964fb2e87a373b33b373a78e2b"),  
            {  
                name: "HMAC",  
                hash: "SHA-256"  
            },  
            false, // 不可提取  
            ["sign"] // 密钥用途  
        );  
  
        // 生成 HMAC  
        const message = (new TextEncoder()).encode("Hello, world!");  
        const signature = await crypto.subtle.sign(  
            "HMAC",  
            key,  
            message  
        );  
  
        // 将 ArrayBuffer 转换为十六进制字符串以便查看  
        const hexString = Array.from(new Uint8Array(signature))  
            .map(byte => byte.toString(16).padStart(2, '0'))  
            .join('');  
  
        console.log("HMAC:", hexString);  
    } catch (err) {  
        console.error("Error:", err);  
    }  
}  
  
generateHMAC();





let aaa=crypto.subtle.digest("SHA-256", (new TextEncoder).encode("397197b8-c1a2-459d-b369-b66f1d68b39f"));
console.log('aaaa', aaa)