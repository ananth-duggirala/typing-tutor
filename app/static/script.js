const POST_SCORE_URL = '/post_score'

function handleInput(speed) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', POST_SCORE_URL, true);
    xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    msg = "speed=" + speed;
    xhr.send(msg);

    xhr.addEventListener('load', reqListener);

    console.log('xhr.responseText:', xhr.responseText);
    console.log('xhr.status:', xhr.status);
}
function reqListener() {
//    console.log('this.responseText:', this.responseText);
    console.log('this.status:', this.status);
}

const test_mode = document.querySelector('test-mode');
const prompt_text = document.querySelector('prompt-text');
const response_text = document.querySelector('response-text');

function calculateWPM(text_length, time_elapsed, fraction_correct){
    var gross_wpm = 60*text_length/(5*time_elapsed/1000);
    var net_wpm = gross_wpm*fraction_correct;
    return [gross_wpm, net_wpm];
}

function getPrompt(){
    return "In publishing and graphic design";
}

function prompt_fn(){
    var prompt = getPrompt();
    document.getElementById("prompt-text").innerText = prompt;
}

var first_time = true;
var start_time = 0;
var current_time = 0;
var prompt = "";
function countFunction(){
    if(first_time){
        prompt = getPrompt();        
        start_time = performance.now();
        first_time = false;
    }

    var x = document.getElementById("response-text").value;
    var response_length = x.length;
    var prompt_length = prompt.length;

    if(response_length == prompt_length){
        var finish_time = performance.now();
        
        const time_elapsed = finish_time - start_time;
        var fraction_correct = 0
        for (var i=0; i<prompt_length; i++){
            if (x[i] == prompt[i])
                fraction_correct += 1;
        }
        fraction_correct /= prompt_length;
        
        var wpm_metrics = calculateWPM(prompt_length, time_elapsed, fraction_correct);
        var gross_wpm = parseInt(wpm_metrics[0]);
        var net_wpm = parseInt(wpm_metrics[1]);

        document.getElementById("test").innerHTML = "Gross speed: " + gross_wpm + "<br>" + "Net speed: " + net_wpm;
        first_time = true;
        handleInput(net_wpm.toString());
    }

    if (response_length < prompt_length){
        if (current_time == 0)
          current_time = start_time;
        var prev_current_time = current_time;
        var time_now = performance.now();
        
        var fraction_correct = 0;

        var color = new Array(prompt_length); for (let i=0; i<prompt_length; ++i) color[i] = 0;
        for (var i=0; i<response_length; i++){
            if (x[i] == prompt[i]){
                fraction_correct += 1;
                color[i] = 1;
            }
            else
                color[i] = 2;
        }
            fraction_correct /= response_length;

        const prompt_text_selector = document.getElementById("prompt-text")
        var prompt_text_selector_string = prompt;

        var printstring = "";
        for (var i=0; i<prompt_length; i++){
            printstring += '<span class="color-' + color[i] +'">' + prompt_text_selector_string[i] + '</span>';
        }
        prompt_text_selector.innerHTML = printstring;

        if ((time_now - prev_current_time)/1000 > 1){
            current_time = time_now;

            const time_elapsed = current_time - start_time;
                        
            var wpm_metrics = calculateWPM(response_length, time_elapsed, fraction_correct);
            gross_wpm = parseInt(wpm_metrics[0]);
            net_wpm = parseInt(wpm_metrics[1]);

            document.getElementById("test").innerHTML = net_wpm + " WPM";
        }
    }
}