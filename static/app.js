async function tweet() {
    // by default this is a GET
    const conn = await fetch("/tweet")
    const dataFromServer = await conn.text()
    console.log(dataFromServer)
    document.querySelector("#message").innerHTML = dataFromServer
}


async function save() {
    // if other methods (anything but GET) are needed, use the second argument
    console.log(event) // click
    console.log(event.target) // button
    console.log(event.target.form) //

    const theForm = event.target.form
    const conn = await fetch ("/save", {
        method: "POST",
        body: new FormData(theForm)
    })
    const dataFromServer = await conn.json()
    console.log(dataFromServer)
    // document.querySelector("#message").innerHTML = dataFromServer
    document.querySelector("#message").innerHTML = `Hi ${dataFromServer.user_name} ${dataFromServer.user_last_name} ${dataFromServer.user_nickname}`
}

async function likeTweet() {
    console.log("like tweet")
    const conn = await fetch("/api-like-tweet")
    if(conn.ok){
    const data = await conn.json()
    document.querySelector("button").textContent = "heart solid"
    }else{
    console.log("error")
    }
}

async function unlikeTweet() {
    console.log("unlike tweet")
    const conn = await fetch("/api-unlike-tweet")
    if(conn.ok){
    const data = await conn.json()
    document.querySelector("button").textContent = "heart solid"
    }else{
    console.log("error")
    }
}


// function toggle_menu(){
//     const main_menu = document.querySelector(".main_one")
//     console.log(main_menu)
//     if(main_menu.classList.contains("active")){
//         main_menu.classList.remove("active")
//     }else{
//         main_menu.classList.add("active")
//     }
// }