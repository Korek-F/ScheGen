
const main_h1 = document.getElementById("class_name")
console.log(schedule_data)

//creating teachers dictionary
let teachers = {}
    for(i in schedule_data["teachers"]){
    teachers[schedule_data["teachers"][i]["id"]] = schedule_data["teachers"][i]["name"]
    }

//Checking if errors exists
if(schedule_data["error"]){
    main_h1.innerHTML = `Error, lesson number ${schedule_data["source"]["id"]} has no place in schedule. Add more available hours to ${teachers[schedule_data["source"]["techer"]]}`
}else{ 
    //creating classes dictionary
    let classes = {}
    for(i in schedule_data["classes"]){
    classes[schedule_data["classes"][i]["id"]] = schedule_data["classes"][i]["name"]
    }

    //creating select form for classes
    const select_classes_box = document.getElementById("class_select")
    for(i in schedule_data["classes"]){
        if(schedule_data["classes"][i]["name"]){
        select_classes_box.innerHTML += `<option value="${schedule_data["classes"][i]["id"]}">${schedule_data["classes"][i]["name"]}</option>`
        }
    }

    var current_class = Object.keys(classes)[0]
    
    //function thats display schedule by current class
    main_h1.innerHTML = `<h2>${current_class}</h2>`
    const table = document.getElementsByClassName("table")[0]
    function displayClass(){ 
        for(let i=10; i<60; i++){
            document.getElementById(`t${i}`).innerHTML =""
        }
        for(i in schedule_data["classes"]){
            for(lesson in schedule_data["classes"][i]["lessons"]){
                let c_lesson = schedule_data["classes"][i]["lessons"][lesson]

                if(c_lesson["school_class"]==current_class){
                    let cell = document.getElementById(`t${c_lesson["time"]}`)
                    cell.innerHTML =`${c_lesson["subject"]} || ${teachers[c_lesson["techer"]]}`
                }
            }
        }
    }
    
    //function thats display schedule by current teacher
    var current_teacher = Object.keys(teachers)[0];
    function displayTeacher(){ 
        for(let i=10; i<60; i++){
            document.getElementById(`t${i}`).innerHTML =""
        }
        for(i in schedule_data["teachers"]){
        if(schedule_data["teachers"][i]["id"] == current_teacher){
            for(lesson in schedule_data["teachers"][i]["lessons"]){
            let current_lesson = schedule_data["teachers"][i]["lessons"][lesson]
            let cell = document.getElementById(`t${current_lesson["time"]}`)
            cell.innerHTML =`${current_lesson["subject"]} || ${ classes[current_lesson["school_class"]]}`
            
            }
        }
        }
    }


    select_classes_box.addEventListener("click", function(){
        current_class = select_classes_box.value
        main_h1.innerHTML = `<h2>${classes[current_class]}</h2>`
        displayClass()
    });
    
    //creating select form for teachers
    const select_teacher_box = document.getElementById("teacher_select")
    for(i in schedule_data["teachers"]){
        if(schedule_data["teachers"][i]["name"]){
        select_teacher_box.innerHTML += `<option value="${schedule_data["teachers"][i]["id"]}">${schedule_data["teachers"][i]["name"]}</option>`
        }
    }
    teacher_select.addEventListener("click", function(){
        current_teacher = select_teacher_box.value
        main_h1.innerHTML = `<h2>${teachers[current_teacher]}</h2>`
        displayTeacher()
    });

    displayClass()
}