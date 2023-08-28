using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class AmesRev : MonoBehaviour
{
    public float thetaF = 33.7F;
    public float xL = 2.133F;
    public float xR = 2.133F;
    public float yD = 2.133F;
    public float yU = 2.133F;
    public float zB = 0F;
    public float zF = 4.266F;

    private GameObject planeF, planeB, planeL, planeR, planeU, planeD;

    public Texture textureF;
    public Texture textureB;
    public Texture textureL;
    public Texture textureR;
    public Texture textureU;
    public Texture textureD;

    private void UpdateRoom()
    {
        float roomRectW = xL + xR;
        float roomRectH = yD + yU;
        float roomRectD = zB + zF;

        float tanF = Mathf.Tan((float)(thetaF * Mathf.PI / 180.0));

        float kL = zF / (zF - xL * tanF);
        float kR = zF / (zF + xR * tanF);
        float kMax = (kL > kR) ? kL : kR;
        float kMin = (kL > kR) ? kR : kL;

        float tanB = (zB / zF) * tanF;
        float tanU = (kR * yU - kL * yU) / (kR * xR + kL * xL);
        float tanD = -(kR * yD - kL * yD) / (kR * xR + kL * xL);

        float thetaB = (float)(Mathf.Atan(tanB) * 180.0 / Mathf.PI);
        float thetaU = (float)(Mathf.Atan(tanU) * 180.0 / Mathf.PI);
        float thetaD = (float)(Mathf.Atan(tanD) * 180.0 / Mathf.PI);

        float cosF = Mathf.Cos((float)(thetaF * Mathf.PI / 180.0));
        float cosB = Mathf.Cos((float)(thetaB * Mathf.PI / 180.0));
        float cosU = Mathf.Cos((float)(thetaU * Mathf.PI / 180.0));
        float cosD = Mathf.Cos((float)(thetaD * Mathf.PI / 180.0));

        planeR.transform.localScale = new Vector3(kR * roomRectH / 10.0F, 1F, kR * roomRectD / 10.0F);
        planeL.transform.localScale = new Vector3(kL * roomRectH / 10.0F, 1F, kL * roomRectD / 10.0F);

        float tempW;
        tempW = (kR * xR + kL * xL) / cosF;
        planeF.transform.localScale = new Vector3(tempW / 10.0F, 1F, kMax * roomRectH / 10.0F);
        tempW = (kR * xR + kL * xL) / cosB;
        planeB.transform.localScale = new Vector3(tempW / 10.0F, 1F, kMax * roomRectH / 10.0F);
        tempW = (kR * xR + kL * xL) / cosU;
        planeU.transform.localScale = new Vector3(tempW / 10.0F, 1F, kMax * roomRectD / 10.0F);
        tempW = (kR * xR + kL * xL) / cosD;
        planeD.transform.localScale = new Vector3(tempW / 10.0F, 1F, kMax * roomRectD / 10.0F);

        planeF.transform.eulerAngles = new Vector3(90f, 0f, -180f-thetaF);
        planeB.transform.eulerAngles = new Vector3(90f, 0f, thetaB);
        planeR.transform.eulerAngles = new Vector3(90f,-90f, 0f);
        planeL.transform.eulerAngles = new Vector3(90f, 90f, 0f);
        planeU.transform.eulerAngles = new Vector3(0f, 0f, thetaU + 180f);
        planeD.transform.eulerAngles = new Vector3(0f, 180f, -thetaD);

        planeF.transform.position = new Vector3((kR * xR - kL * xL) / 2.0F,
                                                (yU - yD) / 2.0F * kMax,
                                                (kL + kR) / 2.0F * zF);
        planeB.transform.position = new Vector3((kR * xR - kL * xL) / 2.0F,
                                                (yU - yD) / 2.0F * kMax,
                                                (kL + kR) / 2.0F * (-zB));
        planeR.transform.position = new Vector3(kR * xR,
                                                kR * (yU - yD) / 2.0F,
                                                kR * (zF - zB) / 2.0F);
        planeL.transform.position = new Vector3(-kL * xL,
                                                 kL * (yU - yD) / 2.0F,
                                                 kL * (zF - zB) / 2.0F);
        planeU.transform.position = new Vector3((kR * xR - kL * xL) / 2.0F,
                                                (kL + kR) / 2.0F * yU,
                                                (zF - zB) / 2.0F * kMax);
        planeD.transform.position = new Vector3((kR * xR - kL * xL) / 2.0F,
                                                (kL + kR) / 2.0F * (-yD),
                                                kMax * (zF - roomRectD / 2.0F));

        if (textureF != null || zF > 0)
        {   planeF.SetActive(true);
            planeF.GetComponent<Renderer>().material.mainTexture = textureF;    }
        else
            planeF.SetActive(false);
        if (textureB != null || zB > 0)
        {   planeB.SetActive(true);
            planeB.GetComponent<Renderer>().material.mainTexture = textureB;    }
        else
            planeB.SetActive(false);

        if (textureU != null || yU > 0)
        {   planeU.SetActive(true);
            planeU.GetComponent<Renderer>().material.mainTexture = textureU;    }
        else
            planeU.SetActive(false);
        if (textureD != null || yD > 0)
        {   planeD.SetActive(true);
            planeD.GetComponent<Renderer>().material.mainTexture = textureD;    }
        else
            planeD.SetActive(false);
        if (textureR != null || xR > 0)
        {   planeR.SetActive(true);
            planeR.GetComponent<Renderer>().material.mainTexture = textureR;    }
        else
            planeR.SetActive(false);
        if (textureL != null || xL > 0)
        {   planeL.SetActive(true);
            planeL.GetComponent<Renderer>().material.mainTexture = textureL;    }
        else
            planeL.SetActive(false);
    }

    void Awake() {
        planeF = GameObject.CreatePrimitive(PrimitiveType.Plane);
        planeB = GameObject.CreatePrimitive(PrimitiveType.Plane);
        planeL = GameObject.CreatePrimitive(PrimitiveType.Plane);
        planeR = GameObject.CreatePrimitive(PrimitiveType.Plane);
        planeU = GameObject.CreatePrimitive(PrimitiveType.Plane);
        planeD = GameObject.CreatePrimitive(PrimitiveType.Plane);
        UpdateRoom();
    }

    void Start() {
    }

    void Update()
    {
        UpdateRoom();
    }
}
