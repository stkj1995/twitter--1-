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
    const dataFromServer = await conn.text()
    console.log(dataFromServer)
    document.querySelector("#message").innerHTML = dataFromServer
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