
document.body.onload = () =>{
    let ul = document.getElementById("menuItems")
    let lis = ul.children
    let pageTitle = document.title
    for(i of lis)
    {   if(pageTitle===i.firstElementChild.innerText) 
        i.firstElementChild.classList.toggle('active')
    }
}