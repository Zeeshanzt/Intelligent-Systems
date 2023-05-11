let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".sidebarBtn");
let sidebarLinks = document.querySelectorAll(".nav-links li a");
sidebarBtn.onclick = function() {
  sidebar.classList.toggle("active");
  if(sidebar.classList.contains("active")){
  sidebarBtn.classList.replace("bx-menu" ,"bx-menu-alt-right");
}else
  sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
}
// Add click event listener to sidebar links
const button = document.querySelector(".button-process");
    button.addEventListener("click", () =>{
      button.classList.add("active");
      setTimeout(()=>{
        button.classList.remove("active");
        button.querySelector("i").classList.replace("bx-cloud-download", "bx-check-circle")
        button.querySelector("span").innerText = "Completed";
      },6000);
    });