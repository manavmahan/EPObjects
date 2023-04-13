const ProjectsTableName = 'Projects';

const DoesProjectExists = (userName, projectName) => {
    let params = {
        TableName: UsersListTableName,
        Key: {
            'UserName' : {S: `${userName}`},
            'ProjectName' : {S: `${projectName}`},
        }
    };

    client.getItem(params, function(err, data){
        if (err){
            throw err;
        };
        return Boolean(data['Item']);
    });
};

export const UpdateProject = async(userName, projectName, projectData, actionSuccess=()=>{}, actionFail=()=>{}) => {
    console.log(`Requested Create Project: ${userName} - ${projectName}`);

    if (! DoesProjectExists) {
        var params = {
            TableName: ProjectsTableName,
            Item: {
                'UserName' : {S: `${userName}`},
                'ProjectName' : {S: `${projectName}`},
            }
        };
        client.putItem(params, function(err, data) {
            if (err) {
                console.log(`Error: ${JSON.stringify(err)}`);
            } else {
                console.log(`Success: ${JSON.stringify(data)}`);
            };
        });
    };

    if (!projectData) return;

    var params = {
        TableName: ProjectsTableName,
        Item: {
            'UserName' : {S: `${userName}`},
            'ProjectName' : {S: `${projectName}`},
            'ProjectData' : {S: `${projectData}`},
        }
    };

    client.updateItem(params, function(err, data) {
        if (err) {
            console.log(`Error: ${JSON.stringify(err)}`);
        } else {
            console.log(`Success: ${JSON.stringify(data)}`);
        };
    });

    actionSuccess();
}