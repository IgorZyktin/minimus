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
                that._initMouseHandling()
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

            _initMouseHandling: function () {
                let selected = null;
                let nearest = null;
                let dragged = null;

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

                        if (nearest && selected && nearest.node === selected.node) {
                            let link = selected.node.data.link

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
        let sys = arbor.ParticleSystem(1000, 800, 0.5, 0.02)
        sys.renderer = Renderer("#viewport")

        sys.graft({
            nodes: main_data_block.nodes,
            edges: main_data_block.edges
        })
    })

})(this.jQuery)