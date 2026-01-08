import img_coffe from "./img/img_coffe.png"
import Image from "next/image";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="grid  sm:grid-cols-1 md:grid-cols-2 items-center gap-4 p-4 rounded-lg">
        <Image src={img_coffe} alt="La tribuna del café" className="sm:w-64  md:w-full h-full" />
        <p className="hidden sm:block  md:text-4xl uppercase font-mono">Marca la diferencia dentro del mercado ofreciendo tu producto a precios justos distinguiendote dentro del mercado tradicional.</p>
      </div>
      <h1 className="text-[#443324] text-6xl uppercase">LA tribuna del café</h1>
      <p className="text-2xl flex justify-center p-6">En La tribuna del café, nuestra misión es bastante clara: conectamos a productores de café con compradores exigentes que buscan algo más que una simple joya oculta. Detrás de cada productor hay una historia y una pasión que se reflejan en cada grano que venden, ofreciendo productos de alta calidad.
        <br />
        Colaboramos con productores que se dedican a la excelencia y que, a través de prácticas cuidadosas, logran sacar el máximo provecho de sus tierras sin perder su esencia. Cada grano de café que se vende en esta plataforma pasa por una exhaustiva evaluación que se realizan por catadores certificados, asegurando que no solo cumpla con los criterios de calidad, sino que también represente fielmente el carácter único de su origen.
      </p>
    </section>
  );
}
