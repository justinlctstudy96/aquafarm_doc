import express, { Request, Response } from 'express';
import bodyParser from 'body-parser';
import multer from 'multer';
import path from 'path';
import fs from 'fs';

const cameraStorage = multer.diskStorage({
        destination: function (req:any, file:any, cb) {
                const camera = req.url.split('/')[2];
                cb(null, path.resolve(`./uploads/${camera}`));
        },
        filename: function (req:any, file:any, cb) {
                cb(null, `${new Date().toISOString().split('.')[0].replace(/:/g, '-')}.jpg`);
        }
})

const cameraUpload = multer({ storage: cameraStorage })

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const getAll = async (req: Request, res: Response) => {
        const camera0File = './uploads/camera0/';
        const camera1File = './uploads/camera1/';
        const camera2File = './uploads/camera2/';
        const camera3File = './uploads/camera3/';
        const camera4File = './uploads/camera4/';
        const camera5File = './uploads/camera5/';

        let camera0Array: string[] = await fs.promises.readdir(camera0File);
        let camera1Array: string[] = await fs.promises.readdir(camera1File);
        let camera2Array: string[] = await fs.promises.readdir(camera2File);
        let camera3Array: string[] = await fs.promises.readdir(camera3File);
        let camera4Array: string[] = await fs.promises.readdir(camera4File);
        let camera5Array: string[] = await fs.promises.readdir(camera5File);

        const returnObject: {[index: string]: string[] | string} = {
                'Port Purpose': 'AquaGreen',
                'camera0': camera0Array,
                'camera1': camera1Array,
                'camera2': camera2Array,
                'camera3': camera3Array,
                'camera4': camera4Array,
                'camera5': camera5Array,
        };

        res.status(200).send(returnObject);
}

app.get('/', getAll)

const getLatestCamera = async (req: Request, res: Response) => {

}

app.get('/latest/:camera', async(req: Request, res: Response) => {
        const camera = req.params.camera;

        if (camera == "camera0" || camera == "camera1" || camera == "camera2" || camera == "camera3" || camera == "camera4" || camera == "camera5"){
                const cameraDir = await fs.promises.readdir(path.resolve(`./uploads/${camera}`));
                const latestCameraPhoto = cameraDir[cameraDir.length - 1]
                if (latestCameraPhoto){
                        return res.status(200).sendFile(path.resolve(`./uploads/${camera}/${latestCameraPhoto}`));
                }
                return res.status(404).send("no photo yet");
        } else {
                return res.status(400).send("Invalid URL");
        }
})

app.get('/:camera/:time', async (req: Request, res: Response) => {
        const camera = req.params.camera;
        const time = req.params.time;

        if(camera && time){
                if (fs.existsSync(`./uploads/${camera}/${time}`)){
                        return res.status(200).sendFile(path.resolve(`./uploads/${camera}/${time}`));
                }
                return res.status(400).send("Invalid URL");
        } else {
                return res.status(400).send("Invalid URL");
        }
})

app.post('./upload/camera0', cameraUpload.single('camera0'), (req: Request, res: Response) => {
        if(req.file){
                const img = fs.readFileSync(req.file.path);
                return res.status(200).send("Image uploaded");
        }
        return res.status(400).send("Invalid URL");
})

app.post('./upload/camera1', cameraUpload.single('camera1'), (req: Request, res: Response) => {
    if(req.file){
            const img = fs.readFileSync(req.file.path);
            return res.status(200).send("Image uploaded");
    }
    return res.status(400).send("Invalid URL");
})

app.post('./upload/camera2', cameraUpload.single('camera2'), (req: Request, res: Response) => {
    if(req.file){
            const img = fs.readFileSync(req.file.path);
            return res.status(200).send("Image uploaded");
    }
    return res.status(400).send("Invalid URL");
})

app.post('./upload/camera3', cameraUpload.single('camera3'), (req: Request, res: Response) => {
    if(req.file){
            const img = fs.readFileSync(req.file.path);
            return res.status(200).send("Image uploaded");
    }
    return res.status(400).send("Invalid URL");
})

app.post('./upload/camera4', cameraUpload.single('camera4'), (req: Request, res: Response) => {
    if(req.file){
            const img = fs.readFileSync(req.file.path);
            return res.status(200).send("Image uploaded");
    }
    return res.status(400).send("Invalid URL");
})

app.post('./upload/camera5', cameraUpload.single('camera0'), (req: Request, res: Response) => {
    if(req.file){
            const img = fs.readFileSync(req.file.path);
            return res.status(200).send("Image uploaded");
    }
    return res.status(400).send("Invalid URL");
})

const PORT = 8080;

app.listen(PORT, () => {
    console.log(`Listening at http://localhost:${PORT}/`);
});
