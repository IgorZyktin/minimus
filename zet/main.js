(function ($) {
    let Renderer = function (canvas_id) {
        let canvas_element = $(canvas_id)
        let canvas = canvas_element.get(0)
        let ctx = canvas.getContext("2d");
        let particleSystem = null

        let that = {
            init: function (system) {
                particleSystem = system
                particleSystem.screenSize(canvas.width, canvas.height)
                particleSystem.screenPadding(100) // отступ с краёв
                $(window).resize(that.resize)
                that.resize()
                that._initMouseHandling()
            },

            resize: function () {
                let w = $(window).width(),
                    h = $(window).height();
                canvas.width = w;
                canvas.height = h
                particleSystem.screenSize(w, h)
                that.redraw()
            },

            redraw: function () {
                ctx.clearRect(0, 0, canvas.width, canvas.height)

                particleSystem.eachEdge(function (edge, pt1, pt2) {
                    ctx.strokeStyle = "rgba(0,0,0, 1.0)"
                    ctx.lineWidth = 1 + 4 * edge.data.weight
                    ctx.beginPath()
                    ctx.moveTo(pt1.x, pt1.y)
                    ctx.lineTo(pt2.x, pt2.y)
                    ctx.stroke()
                })

                particleSystem.eachNode(function (node, pt) {
                    let w = ctx.measureText(node.data.label || "").width + 10
                    let h = 25;
                    let label = node.data.label

                    if (node.data.bg_color) ctx.fillStyle = node.data.bg_color;
                    else ctx.fillStyle = "#5a0000"

                    roundRect(ctx, pt.x - w / 2, pt.y - h / 2, w, h, 5, "#5a0000", 2)

                    if (label) {
                        ctx.font = "bold 16px Arial"
                        ctx.textAlign = "center"
                        ctx.fillStyle = "#d7d7d7"
                        ctx.fillText(label || "", pt.x, pt.y + 5)
                    }
                })
            },
            _initMouseHandling: function () {
                let selected = null;
                let nearest = null;
                let dragged = null;

                let handler = {
                    moved: function (e) {
                        let pos = canvas_element.offset();
                        let _mouseP = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)
                        nearest = particleSystem.nearest(_mouseP);

                        if (!nearest || !nearest.node) return false
                        selected = (nearest.distance < 50) ? nearest : null
                        return false
                    },
                    clicked: function (e) {
                        var pos = $(canvas).offset();
                        _mouseP = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)
                        nearest = dragged = particleSystem.nearest(_mouseP);

                        if (nearest && selected && nearest.node === selected.node) {
                            var link = selected.node.data.link

                            if (link !== undefined) {
                                if (link.match(/^#/)) {
                                    $(that).trigger({
                                        type: "navigate",
                                        path: link.substr(1)
                                    })
                                } else {
                                    window.location = link
                                }
                                return false
                            }

                        }


                        if (dragged && dragged.node !== null) dragged.node.fixed = true

                        $(canvas).unbind('mousemove', handler.moved);
                        $(canvas).bind('mousemove', handler.dragged)
                        $(window).bind('mouseup', handler.dropped)

                        return false
                    },
                    dragged: function (e) {
                        var old_nearest = nearest && nearest.node._id
                        var pos = $(canvas).offset();
                        var s = arbor.Point(e.pageX - pos.left, e.pageY - pos.top)

                        if (!nearest) return
                        if (dragged !== null && dragged.node !== null) {
                            var p = particleSystem.fromScreen(s)
                            dragged.node.p = p
                        }

                        return false
                    },

                    dropped: function (e) {
                        if (dragged === null || dragged.node === undefined) return
                        if (dragged.node !== null) dragged.node.fixed = false
                        dragged.node.tempMass = 1000
                        dragged = null;
                        // selected = null
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
        let sys = arbor.ParticleSystem(1000, 800, 0.5, 0.015)
        sys.renderer = Renderer("#viewport")

        sys.graft({
            nodes: main_data_block.nodes,
            edges: main_data_block.edges
        })
    })

})(this.jQuery)