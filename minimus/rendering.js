function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    // функция рендеринга прямоугольника со сглаженными краями
    if (typeof stroke === 'undefined') {
        stroke = true;
    }
    if (typeof radius === 'undefined') {
        radius = 5;
    }
    if (typeof radius === 'number') {
        radius = {
            tl: radius,
            tr: radius,
            br: radius,
            bl: radius
        };
    } else {
        let defaultRadius = {
            tl: 0,
            tr: 0,
            br: 0,
            bl: 0
        };
        for (let side in defaultRadius) {
            radius[side] = radius[side] || defaultRadius[side];
        }
    }

    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();

    if (fill) {
        ctx.fill();
    }

    if (stroke) {
        ctx.stroke();
    }
}

function drawEdge(ctx, edge, pt1, pt2) {
    // нарисовать одну соединительную линию между блоками
    ctx.strokeStyle = "rgba(0,0,0, 1.0)"
    ctx.lineWidth = 1 + 4 * edge.data.weight
    ctx.beginPath()
    ctx.moveTo(pt1.x, pt1.y)
    ctx.lineTo(pt2.x, pt2.y)
    ctx.stroke()
}


function drawNode(ctx, node, pt) {
    // нарисовать одну ноду
    let w;
    let h;
    let padding = 5;
    [w, h] = drawText(ctx, pt.x, pt.y, padding, node.data.label || '', '#D7D7D7');

    ctx.fillStyle = node.data.bg_color;
    roundRect(
        ctx,
        pt.x - w / 2 - padding,
        pt.y - h / 2 - padding,
        w + padding * 2,
        h + padding * 2,
        5,
        node.data.bg_color,
        2
    );

}


function drawText(ctx, x, y, padding, text, fill) {
    // сделать надпись
    let font_size = 16;
    let w;
    let h = font_size;
    let lines;

    ctx.font = 'bold ' + font_size + 'px Arial';
    ctx.textAlign = 'center';

    if (text.length > 20) lines = text.split(',')
    else lines = [text];

    let longest_line = '';
    for (let line of lines) {
        if (line.trim().length > longest_line.length)
            longest_line = line.trim();
    }
    w = ctx.measureText(longest_line).width + padding * 2;
    let full_h = lines.length * h + padding * 2;

    ctx.fillStyle = fill;
    for (let [index, line] of lines.entries()) {
        ctx.fillText(line.trim(), x, y - full_h / 2 + index * h + h + 3)
    }
    return [w, full_h];
}


(function ($) {
    let Renderer = function (canvas_id) {
        let canvas_element = $(canvas_id)
        let canvas = canvas_element.get(0)
        let ctx = canvas.getContext("2d");
        let particleSystem = null
        let _mouseP

        let that = {
            init: function (system) {
                particleSystem = system
                particleSystem.screenSize(canvas.width, canvas.height)
                particleSystem.screenPadding(100) // отступ с краёв
                $(window).resize(that.resize)
                that.resize()
                that.initMouseHandling()
            },

            resize: function () {
                canvas.width = $(window).width();
                canvas.height = $(window).height()
                particleSystem.screenSize(canvas.width, canvas.height)
                that.redraw()
            },

            redraw: function () {
                ctx.clearRect(0, 0, canvas.width, canvas.height)

                particleSystem.eachEdge(function (edge, pt1, pt2) {
                    drawEdge(ctx, edge, pt1, pt2)
                })

                particleSystem.eachNode(function (node, pt) {
                    drawNode(ctx, node, pt)
                })
            },

            initMouseHandling: function () {
                let selected = null;
                let nearest = null;
                let dragged = null;

                let last_x = 0;
                let last_y = 0;

                let handler = {
                    moved: function (e) {
                        let pos = canvas_element.offset();
                        _mouseP = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)
                        nearest = particleSystem.nearest(_mouseP);

                        if (!nearest || !nearest.node) return false
                        selected = (nearest.distance < 50) ? nearest : null
                        return false
                    },
                    clicked: function (e) {
                        let pos = $(canvas).offset();
                        _mouseP = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)
                        nearest = dragged = particleSystem.nearest(_mouseP);

                        if (dragged && dragged.node !== null) dragged.node.fixed = true

                        last_x = _mouseP.x;
                        last_y = _mouseP.y;

                        $(canvas).unbind('mousemove', handler.moved);
                        $(canvas).bind('mousemove', handler.dragged)
                        $(window).bind('mouseup', handler.dropped)

                        return false
                    },
                    dragged: function (e) {
                        let pos = $(canvas).offset();
                        let s = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)

                        if (!nearest) return
                        if (dragged !== null && dragged.node !== null) {
                            dragged.node.p = particleSystem.fromScreen(s)
                        }
                        return false
                    },

                    dropped: function (e) {
                        if (dragged === null || dragged.node === undefined) return
                        if (dragged.node !== null) dragged.node.fixed = false
                        dragged.node.tempMass = 1000
                        dragged = null;

                        let pos = $(canvas).offset();
                        let s = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)
                        let dist = Math.sqrt(Math.abs(last_x - s.x) + Math.abs(last_y - s.y))

                        if (dist <= 2) {
                            if (nearest && selected && nearest.node === selected.node) {
                                let link = selected.node.data.link

                                if (link !== undefined) {
                                    window.location = link
                                    return false
                                }
                            }
                        }

                        $(canvas).unbind('mousemove', handler.dragged)
                        $(window).unbind('mouseup', handler.dropped)
                        $(canvas).bind('mousemove', handler.moved);
                        _mouseP = null
                        return false
                    }
                }
                $(canvas).mousedown(handler.clicked);
                $(canvas).mousemove(handler.moved);

            }
        }
        return that
    }

    $(document).ready(function () {
        let sys = arbor.ParticleSystem({
            repulsion: 1000,
            stiffness: 600,
            friction: 0.5,
            gravity: false,
            fps: 55,
            df: 0.02,
            precision: 0.6
        })
        sys.renderer = Renderer('#viewport')

        sys.graft({
            nodes: main_data_block.nodes,
            edges: main_data_block.edges
        });

        function zoom(event) {
            event.preventDefault();
            console.log(event)
            console.log(sys.screen())
                    let canvas_element = $('#viewport')
        let canvas = canvas_element.get(0)
        let ctx = canvas.getContext("2d");
            sys.eachNode(function (node, pt) {
                        ctx.fillStyle = '#FF0000';
    roundRect(
        ctx,
        pt.x - 5,
        pt.y - 5,
        10,
        10,
        5,
        '#FFFF00',
        2
    );
                })

        }

        const viewport = document.getElementById('viewport');
        viewport.onwheel = zoom;
        viewport.addEventListener('wheel', zoom);
    });

})(this.jQuery)
