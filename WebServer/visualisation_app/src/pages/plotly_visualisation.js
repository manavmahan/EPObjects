const colors = {Wall:'#874251', intWall:'#994251', Window:'#0288d1', Floor:'#c39b77', Ceiling:'#121414', Roof:'#c9c062', site:'#77ab59'}
const opacity = {Wall: 0.9, intWall:0.1, Window:0.3, Floor:1.0, Ceiling:1.0, Roof:1.0, site:0.5}

function GenerateXYZs(element){
    let xyzs = element['XYZs'].split(',').slice(1);
    element['xs'] = []
    element['ys'] = []
    element['zs'] = []

    while (xyzs.length>0){
        element['xs'].push(xyzs.shift(1));
        element['ys'].push(xyzs.shift(1));
        element['zs'].push(xyzs.shift(1));
    }
}

export default function GenerateBuildingElements(buildingElements)
{
    const plotData = []
    buildingElements.forEach(e => GenerateXYZs(e));
    const [xa, ya, za] = buildingElements.map(e => [Math.max(e['xs']), Math.max(e['ys']), Math.max('zs')]);

    const layoutBui = { 
        'scene':{
            'xaxis': { 'visible': false, 'range': [-1, xa], },
            'yaxis': { 'visible': false, 'range': [-1, ya], },
            'zaxis': { 'visible': false, 'range': [-1, za], },
            'aspectratio':{'x':1, 'y':ya/xa, 'z':za/ya},
            'camera': {
                'up': {'x':0, 'y':0, 'z':1},
                'center': {'x':0, 'y':-.3, 'z':0},
                'eye': {'x':1.8, 'y':-1.2, 'z':0.25},
            }
        },
        'paper_bgcolor':"rgba(0,0,0,0)",
        'plot_bgcolor':"rgba(0,0,0,0)",
        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
        'hovermode': false,
    }

    const config = {displayModeBar:false, responsive: true};

    buildingElements.forEach(e => {
        let del = 'z';
        if (e['xs'].every(a=>a===e['xs'][0]))
            del = 'x';
        if (e['ys'].every(a=>a===e['ys'][0]))
            del = 'y';
        
        let face = {
            type: 'mesh3d',
            x: e['xs'],
            y: e['ys'],
            z: e['zs'],
            delaunayaxis: del,
            color: colors[e.SurfaceType],
            opacity: opacity[e.SurfaceType]
        };
        plotData.push(face);
    });
    return {PlotData: plotData, Layout: layoutBui, Config:config};
}