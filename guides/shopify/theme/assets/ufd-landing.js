(function(){
var f=document.getElementById('ufd-form');
if(f){f.addEventListener('submit',function(e){
var em=f.querySelector('[name="contact[email]"]'),c=document.getElementById('g-consent'),err=document.getElementById('gate-err');
if(!em||!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em.value.trim())){e.preventDefault();err.textContent='Please enter a valid email address.';return;}
if(!c.checked){e.preventDefault();err.textContent='Please tick the box so we can email you.';}
});}
document.addEventListener('ufd:unlocked',function(){var t=document.getElementById('top-cta');if(t){t.textContent='Your planner';}});
})();