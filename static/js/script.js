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
    wrapper.style.backgroundColor = "rgb("+color[0]+","+color[1]+","+color[2]+")";
}

function main()
{
    mainImage = document.getElementById("contentImage");
    mainImage.addEventListener('click', ()=>{
        mainImage.classList.toggle("enlarged")
    });
    let allIcons = document.querySelectorAll('.iconDiv');
    allIcons.forEach(function(icon, index){
        if(index == 6)
        {
            icon.addEventListener('click', ()=>{
                icon.classList.toggle('active');
                if(localStorage.getItem('icon'+index) == 'true')
                {
                    localStorage.removeItem('icon'+index);
                    img.removeEventListener('load', colorSteal);
                    wrapper.style.backgroundColor = 'transparent'
                }
                else
                {
                    localStorage.setItem('icon'+index, 'true');
                    img.addEventListener('load', colorSteal);
                }
            });
        }
        else
        {
            icon.addEventListener('click', ()=>{
                    icon.classList.toggle('active');
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