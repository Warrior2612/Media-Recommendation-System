function switchActive()
{
    const login_text = document.getElementById("login_text");
    const register_text = document.getElementById("register_text");
    const active_line = document.getElementById("active_line");
    const form = document.getElementById("box");
    login_text.addEventListener("click", ()=>{
        active_line.classList.remove("right");
        form.classList.remove("right_active");
    });
    register_text.addEventListener("click", ()=>{
        active_line.classList.add("right");
        form.classList.add("right_active");
    });
}

function colorSteal()
{
    color = colorThief.getColor(img);
    wrapper.style.backgroundImage = "none";
    wrapper.style.backgroundColor = "rgb("+color[0]+","+color[1]+","+color[2]+")";
}

function main()
{
    var i = 0;
    mainImage = document.getElementById("contentImage");
    hiddenContent = document.getElementById("hiddenContent");
    mainImage.addEventListener('click', ()=>{
        hiddenContent.classList.toggle("active")
    });
    hiddenContent.addEventListener('click', ()=>{
        hiddenContent.classList.toggle("active")
    });
    let allIcons = document.querySelectorAll('.iconDiv');
    allIcons.forEach(function(icon, index){
        if(index == 6)
        {
            icon.addEventListener('click', ()=>{
                icon.classList.toggle('active');
                if(i == 1)
                {
                    localStorage.removeItem('icon'+index);
                    img.removeEventListener('load', colorSteal);
                    wrapper.style.backgroundColor = 'transparent';
                    wrapper.style.backgroundImage = 'inherit';
                    i = 0;
                }
                else if(i == 0)
                {
                    localStorage.setItem('icon'+index, 'true');
                    img.addEventListener('load', colorSteal);
                    i = 1;
                }
            });
        }
        else
        {
            icon.addEventListener('click', ()=>{
                    icon.classList.toggle('fa-lg')
                    setTimeout(function(){ icon.classList.toggle('fa-lg') }, 100);
                    if(localStorage.getItem('icon'+index) == 'true')
                    {
                        localStorage.removeItem('icon'+index);
                    }
                    else
                    {
                        localStorage.setItem('icon'+index, 'true');
                    }
                    
                });
            }
    });
}