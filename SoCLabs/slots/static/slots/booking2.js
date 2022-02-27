const table = document.querySelector('.booking-table');
const tableBody = document.getElementsByTagName('tbody')[0];
const slots = document.querySelectorAll('.slot:not(.unavailable)');
const daySelect = document.getElementById('days');


// const data = JSON.parse(document.getElementById('data'))
// for(i=0;i<data.time_schedules.length;i++){
//         var row = document.createElement("tr")
            
//         // inserting time header
//         var header = document.createElement('th')
//         var time_slot = data.time_schedules[i].time_slot
//         var header_text = time_slot.start_time_hours+":"+time_slot.start_time_minutes+"-"+time_slot.end_time_hours+":"+time_slot.end_time_minutes
//         header.appendChild(header_text)
//         row.appendChild(header)
    
//         // inserting board entries
//         for(j=0;j<data.boards.length;j++){
//             board = data.boards[j]
//             if(board.time_slot==time_slot){

//             }
//         }
    
// }

populateUI();
// populating the UI when rendered/reloaded
function populateUI(){
    var bookedSlots = JSON.parse(localStorage.getItem('bookedSlots'));
    if(bookedSlots!=null && bookedSlots!=undefined){
        console.log(bookedSlots.length);
        bookedSlots.forEach(slot => {
            var cell = table.rows[slot[0]].cells[slot[1]]; 
            cell.classList.add('booked');
            cell.innerText = "zzz_rno";    
        });
    }
}
// update Local Storage
function updateLocalStorage(){
    var selectedSlot = document.querySelector('.slot.selected');
    var slotRowIndex = selectedSlot.parentElement.rowIndex;
    var slotCellIndex = selectedSlot.cellIndex;
    var selectedIndex = [slotRowIndex,slotCellIndex];
    var bookedIndex = localStorage.getItem('bookedSlots');
    if(bookedIndex==null || bookedIndex==undefined){
        bookedIndex=[];
    }
    bookedIndex.push(selectedIndex);
    localStorage.setItem('bookedSlots',JSON.stringify(bookedIndex));

}
// update local storage 
function updateTimingForm(){
    var selectedSlot = document.querySelector('.slot.selected');
    var slotRowIndex = selectedSlot.parentElement.rowIndex;
    var slotCellIndex = selectedSlot.cellIndex;
    var board = document.getElementsByTagName('tr')[0].cells[slotCellIndex].innerText[6];
    var time = selectedSlot.parentElement.cells[0].innerText;

    console.log("Board:"+board+", Time:"+time);
    document.getElementById('time-slot').value = time;
    document.getElementById('board').value = board;
}
// clearing the previously selected slot 
function clearSelections(){
    for(var i=0;i<slots.length;i++){
        if(slots[i].classList.contains('selected')){
            slots[i].classList.remove('selected');
        }
    }
}
//slot click event
table.addEventListener('click',(e) => {
    if(e.target.classList.contains('slot') && !e.target.classList.contains('unavailable')){
        clearSelections();
        e.target.classList.toggle('selected');
        updateTimingForm();
    }
})

// submit button clicked
document.getElementsByClassName('btn-timing-submit')[0].addEventListener('click',(e) => {
    updateLocalStorage();
    document.getElementById('time-slot').value = "";
    document.getElementById('board').value = "";
})

// clear button clicked
document.getElementsByClassName('btn-clear')[0].addEventListener("click",(e) => {
    clearSelections();
    document.getElementById('time-slot').value = "";
    document.getElementById('board').value = "";
})