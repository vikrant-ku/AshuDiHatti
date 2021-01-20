const initBg = (autoplay = true) => {
    const bgImgsNames = ['diagoona-bg-1.jpg', 'diagoona-bg-2.jpg', 'diagoona-bg-3.jpg'];
    const bgImgs = bgImgsNames.map(img => "img/" + img);

    $.backstretch(bgImgs, {duration: 4000, fade: 500});

    if(!autoplay) {
      $.backstretch('pause');  
    }    
}

const setBg = id => {
    $.backstretch('show', id);
}

const setBgOverlay = () => {
    const windowWidth = window.innerWidth;
    const bgHeight = $('body').height();
    const tmBgLeft = $('.tm-bg-left');

    $('.tm-bg').height(bgHeight);

    if(windowWidth > 768) {
        tmBgLeft.css('border-left', `0`)
                .css('border-top', `${bgHeight}px solid transparent`);                
    } else {
        tmBgLeft.css('border-left', `${windowWidth}px solid transparent`)
                .css('border-top', `0`);
    }
}

$(document).ready(function () {
    const autoplayBg = true;	// set Auto Play for Background Images
    initBg(autoplayBg);    
    setBgOverlay();

    const bgControl = $('.tm-bg-control');            
    bgControl.click(function() {
        bgControl.removeClass('active');
        $(this).addClass('active');
        const id = $(this).data('id');                
        setBg(id);
    });

    $(window).on("backstretch.after", function (e, instance, index) {        
        const bgControl = $('.tm-bg-control');
        bgControl.removeClass('active');
        const current = $(".tm-bg-controls-wrapper").find(`[data-id=${index}]`);        
        current.addClass('active');
    });

    $(window).resize(function() {
        setBgOverlay();
    });
});
// Cambio section al click
$('button').click(function(){
  actualSection = (actualSection >= totalSection) ? 1 : ++actualSection;
  $('#pieces').removeAttr('class').addClass('section' + actualSection);
  morphingPaths(actualSection);
});

// window resize
$(window).on('resize', function(){
  morphingPaths(actualSection);
}).resize();

// Morphing Paths
function morphingPaths(section) {
  sections();
  var $path1 = $('#path1'),
      $path2 = $('#path2');
  
  switchToPath($path1, section, 'path1');
  setTimeout(function(){
    switchToPath($path2, section, 'path2');
  }, 200);
}

function switchToPath($path, section, sectionPath) {
  var pathPoints = eval('section' + section)[sectionPath];
  var points = '';
  
  window[sectionPath] = []; // reset var path1/path2
  actualPoints = $path.attr('points').split(' ');  // punti corretti dell'svg
  
  
  // creo un oggetto path1 / path2 che abbia i punti iniziali e finali
  for (var i = 0; i < pathPoints.length; i++) {
    actualPoint = actualPoints[i].split(',');
    
    obj = {
      x: actualPoint[0],
      endX: pathPoints[i].x,
      y: actualPoint[1],
      endY: pathPoints[i].y
    }
    
    // path1 / path2
    window[sectionPath].push(obj);
  }
  
  // animo con GSAP
  for (var i = 0; i < window[sectionPath].length; i++) {
    p = window[sectionPath][i];
    
    console.log(p.x);
    
    TweenMax.to(p, 1, {
      x: p.endX,
      y: p.endY,
      ease: Expo.easeInOut,
      delay: i * .25,
      onUpdate: function(){
        animatePath($path, window[sectionPath]);
      }
     }, .2);
  }
  
  function animatePath($path, path) {
    var points = '';
    for (var i = 0; i < path.length; i++) {
      var point = path[i].x + ',' + path[i].y;
      points += point + ' ';
    }
    $path.attr('points', points);
  }
}