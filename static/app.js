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
    document.querySelector("#like_tweet").classList.toggle("hidden")
    document.querySelector("#unlike_tweet").classList.toggle("hidden")
    }else{
    console.log("error")
    }
}

async function unlikeTweet() {
    console.log("unlike tweet")
    const conn = await fetch("/api-unlike-tweet")
    if(conn.ok){
    const data = await conn.json()
    document.querySelector("#like_tweet").classList.toggle("hidden")
    document.querySelector("#unlike_tweet").classList.toggle("hidden")
    }else{
    console.log("error")
    }
}

let currentPage = 1;

async function showMoreTweets() {
    currentPage++;  // next page
    const conn = await fetch(`/api-get-tweets?page=${currentPage}`);
    if (conn.ok) {
        const html = await conn.text();
        // mixhtml syntax: append new tweets and replace the button
        document.querySelector("#tweets").insertAdjacentHTML("beforeend", html);

        // optionally, check if there’s still a #show_more link
        if (!document.querySelector("#show_more a")) {
            document.getElementById("show_more").style.display = "none";
        }
    } else {
        console.log("Error loading more tweets");
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