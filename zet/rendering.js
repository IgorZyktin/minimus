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
    let w = ctx.measureText(node.data.label || "").width + 10
    let h = 25;
    let label = node.data.label

    ctx.fillStyle = node.data.bg_color;

    roundRect(ctx, pt.x - w / 2, pt.y - h / 2, w, h, 5, node.data.bg_color, 2)

    if (label) {
        ctx.font = "bold 16px Arial"
        ctx.textAlign = "center"
        ctx.fillStyle = "#d7d7d7"
        ctx.fillText(label || "", pt.x, pt.y + 5)
    }
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
            gravity: true,
            fps: 55,
            df: 0.02,
            precision: 0.6
        })
        sys.renderer = Renderer("#viewport")

        sys.graft({
            nodes: main_data_block.nodes,
            edges: main_data_block.edges
        })
    })

})(this.jQuery)