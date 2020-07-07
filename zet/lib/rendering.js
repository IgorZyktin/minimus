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

    if (node.data.bg_color) ctx.fillStyle = node.data.bg_color;
    else ctx.fillStyle = "#5a0000"

    roundRect(ctx, pt.x - w / 2, pt.y - h / 2, w, h, 5, "#5a0000", 2)

    if (label) {
        ctx.font = "bold 16px Arial"
        ctx.textAlign = "center"
        ctx.fillStyle = "#d7d7d7"
        ctx.fillText(label || "", pt.x, pt.y + 5)
    }
}